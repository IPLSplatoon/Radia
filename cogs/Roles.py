"""
Deals with all roles related commands and functions
"""
import utils
from discord.ext import commands, tasks
import discord
import gSheetConector
import battlefyConnector


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sheets = gSheetConector.SheetConnector("files/Low Ink Bot-c125c84051d8.json", "Low Ink Bot DataSet")
        self.settings = self.sheets.get_settings("Settings")
        self.battlefy = battlefyConnector.BattlefyUtils()
        self.roles = self.sheets.get_self_assign_roles("AssignableRoles")

    @tasks.loop(hours=12)
    async def update(self):
        self.settings = self.sheets.get_settings("Settings")  # Update settings
        self.roles = self.sheets.get_self_assign_roles("AssignableRoles")
        for server in self.bot.guilds:
            if server.id in self.settings:
                await self.__assignCaptainRole(server.id)  # Update roles

    async def __assignCaptainRole(self, serverID: int, channelID: int = 0) -> bool:
        guild = self.bot.get_guild(serverID)
        if guild is None:
            return False
        if str(serverID) in self.settings:
            settings = self.settings[str(serverID)]
            captains = await self.battlefy.get_custom_field(settings["BattlefyTournamentID"],
                                                            settings["BattlefyFieldID"])
            teamNames = await self.battlefy.get_captains_team(settings["BattlefyTournamentID"],
                                                              settings["BattlefyFieldID"])
            invalidCaptains = captains
            # Gets the role object relating to the server's captain role
            role = discord.utils.get(guild.roles, id=int(settings["CaptainRoleID"]))
            # Remove captain role from all member it
            for member in guild.members:
                if role in member.roles:
                    await member.remove_roles(role)
                    await member.edit(nick=None)  # We remove their nickname as well
            # Assign the captain role to current signed up captains
            for member in guild.members:
                username = "{}#{}".format(member.name, member.discriminator)
                if username in captains:
                    await member.add_roles(role, reason="Add captain role")
                    await member.edit(nick=teamNames[username])
                    invalidCaptains.remove(username)
            # From here we get the channel in guild we want to post update to and send an update embed
            if channelID == 0:
                channelID = int(settings["BotChannelID"])
            replyChannel = discord.utils.get(guild.text_channels, id=channelID)
            embed = await utils.embeder.create_embed("Assign Captain Role", "Report of assigning captain roles")
            embed.add_field(name="Status:", value="Complete", inline=True)
            if invalidCaptains:  # If the list of invalid captains in not empty, we failed to assign all roles
                # Following creates a code block in a str
                captainNotAssigned = "```\n"
                for x in invalidCaptains:
                    captainNotAssigned = captainNotAssigned + "- {} | {}\n".format(x, teamNames[x])
                captainNotAssigned = captainNotAssigned + "```"
                # Add field to embed
                embed.add_field(name="Unable to assign to:", value=captainNotAssigned, inline=False)
            await replyChannel.send(embed=embed)  # send embed
            return True
        else:
            return False

    @commands.has_role("Staff")  # Limits to only staff being able to use command
    @commands.command(name='assignCaptain', help="Give Captains on battlefy the Captains role",
                      aliases=["captain", "Captains"])
    async def assignCap(self, ctx):
        self.settings = self.sheets.get_settings("Settings")
        await self.__assignCaptainRole(ctx.message.guild.id, ctx.message.channel.id)

    @commands.command(name='role', help="Give yourself a role", aliases=["rank", "assign"])
    async def autoAssign(self, ctx, role="listAll"):
        if role == "listAll":
            embed = await utils.embeder.create_embed("Role", "List the roles you can assign yourself")
            rulesList = await utils.embeder.list_to_code_block(self.roles[ctx.message.guild.id])
            embed.add_field(name="Roles", value=rulesList, inline=False)
            await ctx.send(embed=embed)
        else:
            role = role.title()
            if role in self.roles[ctx.message.guild.id]:
                roleToAssign = discord.utils.get(ctx.message.guild.roles, name=role)
                botRole = discord.utils.get(ctx.message.guild.roles, name="TourneyLeague")
                if roleToAssign:  # check if role exists
                    if roleToAssign < botRole:  # Check if role being assigned is bellow the bot
                        embed = await utils.embeder.create_embed("Role", "Role Assigned/Removed")
                        if roleToAssign in ctx.message.author.roles:
                            await ctx.message.author.remove_roles(roleToAssign, reason="Role {} requested".format(role))
                            embed.add_field(name="Removed:", value=role, inline=False)
                            await ctx.send(embed=embed)
                        else:
                            await ctx.message.author.add_roles(roleToAssign, reason="Role {} requested".format(role))
                            embed.add_field(name="Added:", value=role, inline=False)
                            await ctx.send(embed=embed)

    @commands.has_role("Staff")
    @commands.command(name='updateRoles', help="Update settings and self assign roles")
    async def updateStorage(self):
        self.settings = self.sheets.get_settings("Settings")
        self.roles = self.sheets.get_self_assign_roles("AssignableRoles")


def setup(bot):
    bot.add_cog(Roles(bot))
