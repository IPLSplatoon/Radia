"""
Deals with all roles related commands and functions
"""
import utils
from discord.ext import commands, tasks
import discord
import gSheetConnector
import battlefyConnector
import datetime
import copy
import os
from dotenv import load_dotenv

load_dotenv("files/.env")
GOOGLE_SHEET_NAME = os.environ.get("google_sheet_name")


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sheets = gSheetConnector.SheetConnector("files/googleAuth.json", GOOGLE_SHEET_NAME)
        self.settings = self.sheets.get_settings("Settings")
        self.battlefy = battlefyConnector.BattlefyUtils()
        self.roles = self.sheets.get_self_assign_roles("AssignableRoles")
        self.update_roles.start()

    @tasks.loop(hours=8)
    async def update_roles(self):
        self.settings = self.sheets.get_settings("Settings")  # Update settings
        self.roles = self.sheets.get_self_assign_roles("AssignableRoles")
        for server in self.bot.guilds:
            if str(server.id) in self.settings:
                serverSetting = self.settings[str(server.id)]
                if serverSetting["AutoAssignCaptainRole"]:
                    await self.__assign_captain_role(server.id)  # Update roles

    async def __assign_captain_role(self, serverID: int, channelID: int = 0) -> bool:
        """
        Private method, gives captain role to server
        :param serverID: int
            Server id to look through
        :param channelID: int
            Channel ID to post to
        :return: bool
            If successful or not
        """
        try:
            guild = self.bot.get_guild(serverID)
            if guild is None:
                return False
            if str(serverID) in self.settings:
                settings = self.settings[str(serverID)]
                captains = await self.battlefy.get_custom_field(settings["BattlefyTournamentID"],
                                                                settings["BattlefyFieldID"])
                if not captains:
                    return False
                teamNames = await self.battlefy.get_captains_team(settings["BattlefyTournamentID"],
                                                                  settings["BattlefyFieldID"])
                captainCount = copy.deepcopy(len(captains))
                # Gets the role object relating to the server's captain role
                role = discord.utils.get(guild.roles, id=int(settings["CaptainRoleID"]))
                # Remove captain role from all member it
                for member in guild.members:
                    if role in member.roles:
                        await member.remove_roles(role)
                        await member.edit(nick=None)  # We remove their nickname as well
                # Assign the captain role to current signed up captains
                for member in guild.members:
                    username = str(member)
                    if username in captains:
                        await member.add_roles(role, reason="Add captain role")
                        nickname = (teamNames[username])[:32]  # Truncates team made to be 32 char long
                        await member.edit(nick=nickname)
                        captains.remove(username)
                # From here we get the channel in guild we want to post update to and send an update embed
                if channelID == 0:
                    channelID = int(settings["BotChannelID"])
                replyChannel = discord.utils.get(guild.text_channels, id=channelID)
                if replyChannel is None:
                    print("Channel for {} doesn't exist".format(channelID))
                embed = await utils.embedder.create_embed("Assign Captain Role Report")
                embed.add_field(name="Status:", value="Complete", inline=True)
                captainAssignedCount = captainCount - len(captains)
                embed.add_field(name="No. Assigned to:", value=captainAssignedCount, inline=True)
                embed.add_field(name="No. unable Assigned to:", value=len(captains), inline=True)
                if captains:  # If the list of invalid captains in not empty, we failed to assign all roles
                    # Following creates a code block in a str
                    captainNotAssigned = "```\n"
                    for x in captains:
                        captainNotAssigned = captainNotAssigned + "- {} | {}\n".format(x, teamNames[x])
                    captainNotAssigned = captainNotAssigned + "```"
                    # Add field to embed
                    embed.add_field(name="List of captains that failed to be assigned:",
                                    value=captainNotAssigned, inline=False)
                print("Updated captain role for {} at {}".format(serverID, datetime.datetime.utcnow()))
                print("Captains: {} | Unable to assign: {} | Assigned: {}".format(captainCount, len(captains),
                                                                                  captainAssignedCount))
                await replyChannel.send(embed=embed)  # send embed
                return True
            else:
                return False
        except discord.DiscordException as E:
            utils.errorCollector.collect_error(E, "Assign Captain")

    @commands.has_role("Staff")  # Limits to only staff being able to use command
    @commands.guild_only()
    @commands.command(name='assignCaptain', help="Give Captains on battlefy the Captains role",
                      aliases=["captain", "Captains"])
    async def assignCap(self, ctx):
        with ctx.typing():
            self.settings = self.sheets.get_settings("Settings")
            await self.__assign_captain_role(ctx.message.guild.id, ctx.message.channel.id)

    @commands.command(name='role', help="Give yourself a role", aliases=["rank", "assign"])
    @commands.guild_only()
    async def auto_assign(self, ctx, role="listAll"):
        with ctx.typing():
            if role == "listAll":
                embed = await utils.embedder.create_embed("Role", "List the roles you can assign yourself")
                rolesList = await utils.embedder.list_to_code_block(self.roles[ctx.message.guild.id])
                embed.add_field(name="Roles", value=rolesList, inline=False)
                await ctx.send(embed=embed)
            else:
                role = role.title()
                if role in self.roles[ctx.message.guild.id]:
                    roleToAssign = discord.utils.get(ctx.message.guild.roles, name=role)
                    botRole = discord.utils.get(ctx.message.guild.roles, name="Radia")
                    if roleToAssign:  # check if role exists
                        if roleToAssign < botRole:  # Check if role being assigned is bellow the bot for sanity
                            embed = await utils.embedder.create_embed("Role", "Role Assigned/Removed")
                            # If the user already has the role, we remove the role from them
                            if roleToAssign in ctx.message.author.roles:
                                await ctx.message.author.remove_roles(roleToAssign,
                                                                      reason="Role {} requested".format(role))
                                embed.add_field(name="Removed:", value=role, inline=False)
                                await ctx.send(embed=embed)
                            else:  # Else we assign them the role
                                await ctx.message.author.add_roles(roleToAssign,
                                                                   reason="Role {} requested".format(role))
                                embed.add_field(name="Added:", value=role, inline=False)
                                await ctx.send(embed=embed)

    @commands.has_role("Staff")
    @commands.guild_only()
    @commands.command(name='updateRoles', help="Update settings and self assign roles")
    async def update_storage(self, ctx):
        self.settings = self.sheets.get_settings("Settings")
        self.roles = self.sheets.get_self_assign_roles("AssignableRoles")
        await ctx.send("Updated settings and roles list")

    @commands.has_role("Staff")
    @commands.guild_only()
    @commands.command(name='removeChampions', help="Remove the Champion role from users who currently have it",
                      aliases=["dethrone", "removechampions"])
    async def dethrone(self, ctx):
        with ctx.typing():
            removeRole = discord.utils.get(ctx.message.guild.roles, name="Low Ink Current Champions")
            giveRole = discord.utils.get(ctx.message.guild.roles, name="Past Low Ink Winner")
            userList = []
            for member in ctx.message.guild.members:
                if removeRole in member.roles:
                    await member.remove_roles(removeRole)
                    await member.add_roles(giveRole)
                    userList.append(member)
            replyList = "```\n"
            if userList:
                for people in userList:
                    replyList = replyList + "- {}\n".format(people.display_name)
            replyList = replyList + "```"
            embed = await utils.embedder.create_embed("Removed Low Ink Champion Role",
                                                      "Removed the Low Ink Champion Role from members")
            embed.add_field(name="Removed from:", value=replyList, inline=False)
            await ctx.send(embed=embed)

    async def get_member(self, guildID: int, memberID: int) -> discord.member:
        guild = self.bot.get_guild(guildID)
        if guild is None:
            return None
        for member in guild.members:
            if member.id == memberID:
                return member
        return None

    @commands.has_role("Staff")
    @commands.guild_only()
    @commands.command(name='addChampions', help="Add the Champion role to the mentioned user",
                      aliases=["coronate", "addchampions"])
    async def coronate(self, ctx, mention):
        with ctx.typing():
            pastRole = discord.utils.get(ctx.message.guild.roles, name="Past Low Ink Winner")
            currentRole = discord.utils.get(ctx.message.guild.roles, name="Low Ink Current Champions")
            memberID = int(mention[3:][:-1])
            member = await self.get_member(ctx.message.guild.id, memberID)
            if member:
                await member.add_roles(pastRole)
                await member.add_roles(currentRole)
            embed = await utils.embedder.create_embed("Added Champion Role",
                                                      "Added Champion Role to {}".format(mention))
            await ctx.send(embed=embed)

    @commands.has_role("Staff")
    @commands.guild_only()
    @commands.command(name='removeAllCaptains', help="Remove the captains role from everyone with it")
    async def remove_captain(self, ctx, removeNick="False"):
        with ctx.typing():
            if removeNick.upper() in ["TRUE", "YES"]:
                removeNick = True
            else:
                removeNick = False
            settings = self.settings[str(ctx.message.guild.id)]
            role = discord.utils.get(ctx.message.guild.roles, id=int(settings["CaptainRoleID"]))
            for member in ctx.message.guild.members:
                if role in member.roles:
                    await member.remove_roles(role)
                    if removeNick:
                        await member.edit(nick=None)

            embed = await utils.embedder.create_embed("Removed Captain Role",
                                                      "Removed the Captain role from members")
            await ctx.send(embed=embed)

    @commands.has_role("Staff")
    @commands.guild_only()
    @commands.command(name='checkCaptain', help="Internal Debug command", aliases=["checkcaptain"])
    async def check_captain(self, ctx):
        with ctx.typing():
            settings = self.settings[str(ctx.message.guild.id)]
            captains = await self.battlefy.get_custom_field(settings["BattlefyTournamentID"],
                                                            settings["BattlefyFieldID"])
            if not captains:
                return
            teamNames = await self.battlefy.get_captains_team(settings["BattlefyTournamentID"],
                                                              settings["BattlefyFieldID"])
            for member in ctx.message.guild.members:
                if str(member) in captains:
                    captains.remove(str(member))

            embed = await utils.create_embed("Captains not Found", "This is the list of people who will fail "
                                                                   "to have the captain role assigned to them")
            embed.add_field(name="No Players not found:", value=len(captains), inline=False)
            if captains:  # If the list of invalid captains in not empty, we failed to assign all roles
                # Following creates a code block in a str
                captainNotAssigned = "```\n"
                for x in captains:
                    captainNotAssigned = captainNotAssigned + "- {} | {}\n".format(x, teamNames[x])
                captainNotAssigned = captainNotAssigned + "```"
                # Add field to embed
                embed.add_field(name="List of captains that aren't found on the server:",
                                value=captainNotAssigned, inline=False)
            await ctx.send(embed=embed)

    @commands.has_role("Staff")
    @commands.guild_only()
    @commands.command(name='debug', help="Internal Debug command", hidden=True)
    async def debug(self, ctx):
        with ctx.typing():
            with open("debug.txt", "w", encoding="utf-8") as file:
                file.write("Guild Members\n")
                for member in ctx.message.guild.members:
                    username = "{}#{}".format(member.name, member.discriminator)
                    file.write("{} | {}\n".format(username, member.id))
            await ctx.send("Debug saved to server")


def setup(bot):
    bot.add_cog(Roles(bot))
