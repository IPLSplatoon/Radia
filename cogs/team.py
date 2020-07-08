"""
Cog deals with all check in a print of checked in captains/teams
"""
import gSheetConnector
import utils
from discord.ext import commands
import discord
from dotenv import load_dotenv
import os
import DBConnector
from battlefyConnector import BattlefyUtils

load_dotenv("files/.env")
GOOGLE_SHEET_NAME = os.environ.get("google_sheet_name")
DB_CONNECTION_STRING = os.environ.get("DB_String")


async def team_embed(team: DBConnector.TeamObject) -> discord.embeds:
    """
    Create a discord embed with team's information
    :param team: DBConnector.TeamObject
        Team you want an embed for
    :return: discord.embeds
        Returns a discord embed object
    """
    embed = await utils.embedder.create_embed(team.teamName, "Team Info on: {}".format(team.teamName),
                                              "https://battlefy.com/teams/{}".format(team.battlefyID))
    embed.add_field(name="Captain Discord:", value=team.captainDiscord, inline=True)
    embed.add_field(name="Captain FC:", value=team.captainFC, inline=True)
    embed.add_field(name="Join Date:", value=team.joinDate.strftime("%d/%m/%Y, %H:%M"), inline=True)
    # Get the bracket from the numerical value
    bracket = {
        -1: "N/A",
        1: "Alpha",
        2: "Beta",
        3: "Gamma"
    }
    embed.add_field(name="Bracket:", value=bracket.get(team.bracket, "Unknown"), inline=True)
    if team.allowCheckin:
        embed.add_field(name="Checkin:", value=team.captainFC, inline=True)
    else:
        embed.add_field(name="Checkin:", value="Disabled (*{}*)".format(team.captainFC), inline=True)
    embed.add_field(name="SysID: ", value="`{}`".format(team.ID), inline=True)
    if team.teamIcon != "Unknown":
        embed.set_thumbnail(url=team.teamIcon)
    if team.manualPlayers:
        players = "```\n"
        for player in team.manualPlayers:
            players += "- {}\n".format(player)
        players += "```"
        embed.add_field(name="Staff added Players:", value=players, inline=False)
    playerCount = 1
    for player in team.players:
        embed.add_field(name="Player {}:".format(player), value=str(player), inline=False)
        playerCount += 1
    return embed


class Teams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sheets = gSheetConnector.SheetConnector("files/googleAuth.json", GOOGLE_SHEET_NAME)
        self.enableCheckin = False
        self.database = DBConnector.DBConnect(DB_CONNECTION_STRING)
        self.battlefy = BattlefyUtils()

    async def get_details(self, discordGuildID: str):
        """
        Get settings from google sheets for a guild
        :param discordGuildID:
            the id of the discord guild
        :return: str
            the activeTournament, discordField, FCField
        """
        settings = self.sheets.get_settings("Settings")
        if discordGuildID not in settings:
            return None
        settings = settings[discordGuildID]
        activeTournament = settings["BattlefyTournamentID"]
        discordField = settings["BattlefyTournamentID"]
        FCField = settings["BattlefyFCID"]
        return activeTournament, discordField, FCField

    async def get_member(self, guildID: int, memberID: int) -> discord.member:
        """
        Get members object
        :param guildID: int
            guildID the member is in
        :param memberID: int
            the Discord ID of the member you're trying to find
        :return: discord.member
            the member object you're trying to find
        """
        guild = self.bot.get_guild(guildID)
        if guild is None:
            return None
        for member in guild.members:
            if member.id == memberID:
                return member
        return None

    async def check_role(self, guildID: int, roleID: int) -> bool:
        """
        Check if a guild has a role
        :param guildID: int
            guildID the role is in
        :param roleID: int
            the ID of the role you're checking
        :return: bool
            whether the role exists of not
        """
        guild = self.bot.get_guild(guildID)
        if guild is None:
            return False
        for role in guild.roles:
            if role.id == roleID:
                return True
        return False

    @commands.has_role("Staff")
    @commands.guild_only()
    @commands.command(name='loadTeams', hidden=True)
    async def load_teams(self, ctx):
        with ctx.typing():
            activeTournament, discordField, FCField = await self.get_details(str(ctx.message.guild.id))
            teams = await self.battlefy.get_list_of_teams(activeTournament, discordField, FCField)
            if teams:
                for team in teams:
                    await self.database.updateTournamentTeam(team, activeTournament)
                embed = await utils.create_embed("Add Teams", "Teams added to database for active tournament")
                embed.add_field(name="Team Count:", value=len(teams), inline=True)
                await ctx.send(embed=embed)
            else:
                await ctx.send(embed=utils.create_embed("Add Teams Error", "No teams to add"))

    @commands.has_role("Staff")
    @commands.guild_only()
    @commands.command(name='addTournament', hidden=True)
    async def add_tournament(self, ctx, tournamentID, captainRoleID):
        with ctx.typing():
            if not captainRoleID.isdigit():
                await ctx.send(embed=utils.create_embed("Add Tournament Error", "Invalid Captain Role ID"))
                return
            if not await self.check_role(ctx.message.guild.id, int(captainRoleID)):
                await ctx.send(embed=utils.create_embed("Add Tournament Error", "Invalid Captain Role ID"))
                return
            tournament = await self.battlefy.get_tournament(tournamentID)
            response = await self.database.addTournament(tournamentID, tournament.startTime,
                                                         str(ctx.message.guild.id), captainRoleID)
            if response:
                await ctx.send(embed=utils.create_embed("Added Tournament",
                                                        "Tournament with ID {} added".format(tournamentID)))
            else:
                await ctx.send(embed=utils.create_embed("Add Tournament Error",
                                                        "Unable to add to DB, may already exits"))

    @commands.has_role("Staff")
    @commands.guild_only()
    @commands.command(name='toggleCheckin', help="Toggle checkin command", aliases=["togglecheckin"])
    async def enable_checkin(self, ctx):
        if self.enableCheckin:
            self.enableCheckin = False
            await ctx.send(embed=await utils.create_embed("Enable/Disable Checkin", "Checkin Disabled!"))
        else:
            self.enableCheckin = True
            await ctx.send(embed=await utils.create_embed("Enable/Disable Checkin", "Checkin Enabled!"))

    @commands.has_role("Staff")
    @commands.command(name='team', help="Get info on a team(s)\n"
                                        "<query>: The team you want to find\n"
                                        "<queryType>: What to find a team by. Can be ID, teamname or a mention",
                      aliases=["teams"])
    async def get_teams(self, ctx, query, queryType="mention"):
        with ctx.typing():
            activeTournament, discordField, FCField = await self.get_details(str(ctx.message.guild.id))
            if queryType.upper() in ["ID", "TEAMID"]:
                teams = await self.database.get_teams(activeTournament, teamID=query)
            elif queryType.upper() in ["NAME", "TEAMNAME"]:
                teams = await self.database.get_teams(activeTournament, teamName=query)
            else:
                memberID = int(query[3:][:-1])
                member = await self.get_member(ctx.message.guild.id, memberID)
                username = "{}#{}".format(member.name, member.discriminator)
                teams = await self.database.get_teams(activeTournament, captainDiscordUsername=username)
            if teams is None:
                embed = await utils.create_embed("Team Overview Error", "Didn't find any team under you name query!")
                await ctx.send(embed=embed)
                return
            for team in teams:
                embed = await team_embed(team)
                await ctx.send(embed=embed)

    @commands.has_role("Captains")
    @commands.command(name='checkin', help="Checkin your team!")
    async def checkin(self, ctx):
        with ctx.typing():
            if self.enableCheckin:
                activeTournament, discordField, FCField = await self.get_details(str(ctx.message.guild.id))
                team = await self.database.get_teams(activeTournament,
                                                     captainDiscordUsername=str(ctx.message.author))
                if not team:
                    await ctx.send(embed=await utils.create_embed("Team Checkin Error!",
                                                                  "Unable to find your team, head to helpdesk!"))
                    return
                team = team[0]
                if team.allowCheckin:
                    reply = await self.database.set_checkin(True, activeTournament,
                                                            captainDiscordUsername=str(ctx.message.author))
                    if reply:
                        embed = await utils.create_embed("{} is Checked in!".format(team.teamName),
                                                         "You Team has been checked in!",
                                                         "https://battlefy.com/teams/{}".format(team.battlefyID))
                        if team.teamIcon != "Unknown":
                            embed.set_thumbnail(url=team.teamIcon)
                        await ctx.send(embed=embed)
                        return
                    else:
                        embed = await utils.create_embed("Team Checkin Error!",
                                                         "We where unable to check your team `{}` in".format(
                                                             team.teamName),
                                                         "https://battlefy.com/teams/{}".format(team.battlefyID))
                        await ctx.send(embed=embed)
                        return
                else:
                    await ctx.send(embed=await utils.create_embed("Team Checkin Error!",
                                                                  "Your teams `{}` isn't enabled to checkin!\n"
                                                                  "Head to helpdesk if this is an error".format(
                                                                      team.teamName)))
            else:
                embed = await utils.create_embed("Team Checkin Closed",
                                                 "Checkin are not enabled at the moment")
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Teams(bot))
