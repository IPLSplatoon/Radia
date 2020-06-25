"""
Cog deals with all check in a print of checked in captains/teams
"""
import gSheetConnector
import utils
from discord.ext import commands, tasks
import discord
from dotenv import load_dotenv
import os
import DBConnector
from battlefyConnector import Team, Player

load_dotenv("files/.env")
GOOGLE_SHEET_NAME = os.environ.get("google_sheet_name")


class Teams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sheets = gSheetConnector.SheetConnector("files/googleAuth.json", GOOGLE_SHEET_NAME)
        self.enableCheckin = False
        settings = self.sheets.get_settings("Settings")
        settings = settings["406137039285649428"]
        self.database = DBConnector.TeamDB(settings["BattlefyTournamentID"], settings["BattlefyFieldID"],
                                           settings["BattlefyFCID"])

    @commands.has_role("Staff")
    @commands.guild_only()
    @commands.command(name='loadTeams', hidden=True)
    async def load_teams(self, ctx):
        if await self.database.add_teams():
            await ctx.send(embed=await utils.create_embed("Load teams", "Teams now loaded into DB"))

    @commands.has_role("Staff")
    @commands.guild_only()
    @commands.command(name='enableCheckin', help="Enable checkin command")
    async def enable_checkin(self, ctx):
        if self.enableCheckin:
            self.enableCheckin = False
            await ctx.send(embed=await utils.create_embed("Enable/Disable Checkin", "Checkin Disabled!"))
        else:
            self.enableCheckin = True
            await ctx.send(embed=await utils.create_embed("Enable/Disable Checkin", "Checkin Enabled!"))

    async def get_member(self, guildID: int, memberID: int) -> discord.member:
        guild = self.bot.get_guild(guildID)
        if guild is None:
            return None
        for member in guild.members:
            if member.id == memberID:
                return member
        return None

    async def team_embed(self, team: Team) -> discord.embeds:
        embed = await utils.embedder.create_embed(team.teamName, "Team Info on: {}".format(team.teamName),
                                                  "https://battlefy.com/teams/{}".format(team.teamID))
        embed.add_field(name="Team Captain:", value=team.captain.inGameName, inline=True)
        embed.add_field(name="Captain Discord:", value=team.captainDiscord, inline=True)
        if self.enableCheckin:
            embed.add_field(name="Day 2 Checkin:", value=team.checkin, inline=True)
        else:
            embed.add_field(name="Day 2 Checkin:", value="N/A", inline=True)
        embed.add_field(name="Captain FC:", value=team.captainFC, inline=False)
        embed.add_field(name="Team ID:", value="`{}`".format(team.teamID), inline=False)
        if team.teamIconURL != "Unknown":
            embed.set_thumbnail(url=team.teamIconURL)
        playerCount = 1
        for player in team.players:
            playerstr = "```\n" \
                        "In Game Name: {}\n" \
                        "Battlefy Name: {}\n" \
                        "Added @: {}\n" \
                        "ID: {}\n" \
                        "```".format(player.inGameName, player.battlefyUsername,
                                     player.createdAt.strftime("%d/%m/%Y %H:%M:%S"), player.persistentPlayerID)
            embed.add_field(name="Player {}:".format(playerCount), value=playerstr, inline=False)
            playerCount = playerCount + 1
        return embed

    @commands.has_role("Staff")
    @commands.command(name='team', help="Get info on a team(s)")
    async def get_teams(self, ctx, query, queryType="mention"):
        with ctx.typing():
            if queryType.upper() in ["ID", "TEAMID"]:
                teams = await self.database.get_teams(teamID=query)
            elif queryType.upper() in ["NAME", "TEAMNAME"]:
                teams = await self.database.get_teams(teamName=query)
            else:
                memberID = int(query[3:][:-1])
                member = await self.get_member(ctx.message.guild.id, memberID)
                username = "{}#{}".format(member.name, member.discriminator)
                teams = await self.database.get_teams(discordUsername=username)
            if teams is None:
                embed = await utils.create_embed("Team Overview Error", "Didn't find any team under you name query!")
                await ctx.send(embed=embed)
                return
            for team in teams:
                embed = await self.team_embed(team)
                await ctx.send(embed=embed)

    @commands.has_role("Captain")
    @commands.command(name='checkin', help="Checkin your team!")
    async def checkin(self, ctx):
        with ctx.typing():
            if self.enableCheckin:
                checkin = await self.database.update_team_checkin(True, discordUsername=str(ctx.message.author))
                if checkin:
                    embed = await utils.create_embed("Team Checkin Complete", "Your team has now be checked in!")
                    await ctx.send(embed=embed)
            else:
                embed = await utils.create_embed("Team Checkin Closed", "Checkin/out are not enabled at the minute")
                await ctx.send(embed=embed)

    @commands.has_role("Captain")
    @commands.command(name='checkout', help="Checkout your team!")
    async def checkout(self, ctx):
        with ctx.typing():
            if self.enableCheckin:
                checkin = await self.database.update_team_checkin(False, discordUsername=str(ctx.message.author))
                if checkin:
                    embed = await utils.create_embed("Team Checkout Complete", "Your team has now be checked out!")
                    await ctx.send(embed=embed)
            else:
                embed = await utils.create_embed("Team Checkin Closed", "Checkin/out are not enabled at the minute")
                await ctx.send(embed=embed)

    @commands.has_role("Staff")
    @commands.command(name='checkinOverride', help="Allows staff to set checkin for teams")
    async def staff_checkin(self, ctx, checkin, query, queryType="mention"):
        with ctx.typing():
            if checkin.upper() in ["YES", "TRUE", "YEP"]:
                checkinStatus = True
            else:
                checkinStatus = False
            try:
                if queryType.upper() in ["ID", "TEAMID"]:
                    checkin = await self.database.update_team_checkin(checkinStatus, teamID=query)
                elif queryType.upper() in ["NAME", "TEAMNAME"]:
                    checkin = await self.database.update_team_checkin(checkinStatus, teamName=query)
                else:
                    memberID = int(query[3:][:-1])
                    member = await self.get_member(ctx.message.guild.id, memberID)
                    username = "{}#{}".format(member.name, member.discriminator)
                    checkin = await self.database.update_team_checkin(checkinStatus, discordUsername=username)
                if checkin:
                    embed = await utils.create_embed("Team Checkin update Complete",
                                                     "Team with following attributes has been update")
                    embed.add_field(name="Checked in status: ", value=checkinStatus, inline=False)
                    embed.add_field(name="{}: ".format(queryType), value="`{}`".format(query), inline=False)
                    await ctx.send(embed=embed)
                else:
                    embed = await utils.create_embed("Team Checkin Error", "Unable to find team with query provided!")
                    await ctx.send(embed=embed)
            except DBConnector.errors.MoreThenOneError:
                embed = await utils.create_embed("Team Checkin Error", "More then one team returned via Query")
                await ctx.send(embed=embed)

    @commands.has_role("Staff")
    @commands.command(name='checkinList', help="List all checked in teams")
    async def checkin_list(self, ctx):
        with ctx.typing():
            checkedInTeams = await self.database.get_teams(checkIN=True)
            if checkedInTeams is None:
                embed = await utils.create_embed("List of teams checked in!", "No teams checked in!")
                await ctx.send(embed=embed)
                return
            checkedInList = "```\n"
            for team in checkedInTeams:
                checkedInList = checkedInList + "- {}\n".format(team.teamName)
            checkedInList = checkedInList + "```"
            if len(checkedInList) < 2048:
                embed = await utils.create_embed("List of teams checked in!", checkedInList)
                await ctx.send(embed=embed)
            else:
                embed = await utils.create_embed("Listing Error", "Too long to post on discord, check console")
                print(checkedInList)
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Teams(bot))
