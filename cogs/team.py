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
from battlefyConnector import BattlefyUtils
import re
from typing import Optional

load_dotenv("files/.env")
GOOGLE_SHEET_NAME = os.environ.get("google_sheet_name")
DB_CONNECTION_STRING = os.environ.get("DB_String")
mentionExpression = re.compile("<@![0-9]{10,}>")

# Get the bracket from the numerical value
bracketValueDict = {
    -1: "N/A",
    1: "Alpha",
    2: "Beta",
    3: "Gamma"
}


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
    embed.add_field(name="Bracket:", value=bracketValueDict.get(team.bracket, "Unknown"), inline=True)
    if team.allowCheckin:
        embed.add_field(name="Checkin:", value=team.checkin, inline=True)
    else:
        embed.add_field(name="Checkin:", value="Disabled (*{}*)".format(team.checkin), inline=True)
    embed.add_field(name="Sys ID: ", value="`{}`".format(team.ID), inline=True)
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
        embed.add_field(name="Player {}:".format(playerCount), value="```\n{}\n```".format(str(player)), inline=False)
        playerCount += 1
    return embed


class Teams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sheets = gSheetConnector.SheetConnector("files/googleAuth.json", GOOGLE_SHEET_NAME)
        self.settings = self.sheets.get_settings("Settings")
        self.enableCheckin = False
        self.database = DBConnector.DBConnect(DB_CONNECTION_STRING)
        self.battlefy = BattlefyUtils()
        self.update_settings.start()

    @tasks.loop(hours=2)
    async def update_settings(self):
        self.settings = self.sheets.get_settings("Settings")

    async def getUsername(self, guildID: int, mention: str) -> Optional[str]:
        if mentionExpression.match(mention):
            memberID = int(mention[3:][:-1])
            member = await self.get_member(guildID, memberID)
            return "{}#{}".format(member.name, member.discriminator)
        return None

    async def get_details(self, discordGuildID: str):
        """
        Get settings from google sheets for a guild
        :param discordGuildID:
            the id of the discord guild
        :return: str
            the activeTournament, discordField, FCField
        """
        if discordGuildID not in self.settings:
            return None
        settings = self.settings[discordGuildID]
        activeTournament = settings["BattlefyTournamentID"]
        discordField = settings["BattlefyFieldID"]
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
    @commands.command(name='updateSettings', hidden=True)
    async def manual_update_settings(self, ctx):
        with ctx.typing():
            await self.update_settings

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
                await ctx.send(embed=await utils.create_embed("Add Tournament Error", "Invalid Captain Role ID"))
                return
            if not await self.check_role(ctx.message.guild.id, int(captainRoleID)):
                await ctx.send(embed=await utils.create_embed("Add Tournament Error", "Invalid Captain Role ID"))
                return
            tournament = await self.battlefy.get_tournament(tournamentID)
            response = await self.database.addTournament(tournamentID, tournament.startTime,
                                                         str(ctx.message.guild.id), captainRoleID)
            if response:
                await ctx.send(embed=await utils.create_embed("Added Tournament",
                                                        "Tournament with ID {} added".format(tournamentID)))
            else:
                await ctx.send(embed=await utils.create_embed("Add Tournament Error",
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
                username = await self.getUsername(ctx.message.guild.id, query)
                if not username:
                    await ctx.send(embed=await utils.create_embed("Team Overview Error",
                                                                  "Invalid Mention"))
                    return
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
                                                         "Your team has been checked in!",
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

    @commands.has_role("Staff")
    @commands.guild_only()
    @commands.command(name='checkinList', help="Get the list of teams checked in/out", aliases=["checkinlist"])
    async def checkin_list(self, ctx, bracket="All"):
        with ctx.typing():
            activeTournament, discordField, FCField = await self.get_details(str(ctx.message.guild.id))
            query = await self.database.get_all_teams(activeTournament)
            teams = []
            if bracket.upper() in ["TOP", "ALPHA", "A"]:
                for team in query:
                    if team.allowCheckin and team.bracket == 1:
                        teams.append(team)
            elif bracket.upper() in ["MID", "BETA", "B", "MIDDLE"]:
                for team in query:
                    if team.allowCheckin and team.bracket == 2:
                        teams.append(team)
            elif bracket.upper() in ["BOTTOM", "GAMMA", "G"]:
                for team in query:
                    if team.allowCheckin and team.bracket == 3:
                        teams.append(team)
            elif bracket.upper() in ["ALL"]:
                for team in query:
                    if team.allowCheckin:
                        teams.append(team)
            else:
                await ctx.send(embed=await utils.create_embed("Checkin List Error", "Invalid Bracket"))
                return
            if not teams:
                await ctx.send(embed=await utils.create_embed("Checkin List", "No teams to list"))
                return
            checkoutList = "```\n"
            checkinList = "```\n"
            for team in teams:
                if team.checkin:
                    checkinList += "- {}\n".format(team.teamName)
                else:
                    checkoutList += "- {}\n".format(team.teamName)
            checkoutList += "```"
            checkinList += "```"
            embed = await utils.create_embed("Checkin List for {}".format(bracket), "List of teams checked in/out")
            embed.add_field(name="Teams **YET** to Checkin:", value=checkoutList, inline=False)
            embed.add_field(name="Teams Checked in:", value=checkinList, inline=False)
            await ctx.send(embed=embed)

    @commands.has_role("Staff")
    @commands.command(name='assignBracket', help="Enable checkin & bracket for a team.\n"
                                                 "<bracket>: Bracket the team should go into\n"
                                                 "<query>: The team you want to find\n"
                                                 "<queryType>: What to find a team by. Can be ID, teamName or a mention",
                      aliases=["assignbracket"])
    async def assign_bracket(self, ctx, bracket, query, queryType="mention"):
        with ctx.typing():
            if bracket.upper() in ["TOP", "ALPHA", "A"]:
                assignRole = discord.utils.get(ctx.message.guild.roles, id=717475987821953085)
                bracketInt = 1
            elif bracket.upper() in ["MID", "BETA", "B", "MIDDLE"]:
                assignRole = discord.utils.get(ctx.message.guild.roles, id=717476155590180876)
                bracketInt = 2
            elif bracket.upper() in ["BOTTOM", "GAMMA", "G"]:
                assignRole = discord.utils.get(ctx.message.guild.roles, id=726243712908263484)
                bracketInt = 3
            else:
                await ctx.send(embed=await utils.create_embed("Team Bracket Assignment Error", "Invalid Bracket given"))
                return
            activeTournament, discordField, FCField = await self.get_details(str(ctx.message.guild.id))
            if queryType.upper() in ["ID", "TEAMID"]:
                teams = await self.database.get_teams(activeTournament, teamID=query)
            elif queryType.upper() in ["NAME", "TEAMNAME"]:
                teams = await self.database.get_teams(activeTournament, teamName=query)
            else:
                username = await self.getUsername(ctx.message.guild.id, query)
                if not username:
                    await ctx.send(embed=await utils.create_embed("Team Bracket Assignment Error",
                                                                  "Invalid Mention"))
                    return
                teams = await self.database.get_teams(activeTournament, captainDiscordUsername=username)
            if len(teams) > 1 or not teams:
                await ctx.send(embed=await utils.create_embed("Team Bracket Assignment Error",
                                                              "Query returns more/less then one team"))
                return
            team = teams[0]
            username = team.captainDiscord
            user = None
            for member in ctx.message.guild.members:
                if str(member) == username:
                    user = member
                    break
            if user is None:
                embed = await utils.create_embed("Team Bracket Assignment Error",
                                                 "Captain Member not found in Guild!")
                await ctx.send(embed=embed)
                return
            await user.add_roles(assignRole, reason="Bracket Assignment by {}".format(str(ctx.message.author)))
            if queryType.upper() in ["ID", "TEAMID"]:
                checkinStatus = await self.database.set_allow_checkin(True, activeTournament, teamID=query)
                bracketStatus = await self.database.set_bracket(bracketInt, activeTournament, teamID=query)
            elif queryType.upper() in ["NAME", "TEAMNAME"]:
                checkinStatus = await self.database.set_allow_checkin(True, activeTournament, teamName=query)
                bracketStatus = await self.database.set_bracket(bracketInt, activeTournament, teamName=query)
            else:
                checkinStatus = await self.database.set_allow_checkin(True, activeTournament,
                                                                      captainDiscordUsername=username)
                bracketStatus = await self.database.set_bracket(bracketInt, activeTournament,
                                                                captainDiscordUsername=username)
            if checkinStatus and bracketStatus:
                embed = await utils.create_embed("Team Bracket Assignment", "Bracket Assignment Complete")
                if team.teamIcon != "Unknown":
                    embed.set_thumbnail(url=team.teamIcon)
                embed.add_field(name="Team: ", value=team.teamName, inline=False)
                embed.add_field(name="Bracket: ", value=bracket, inline=True)
                embed.add_field(name="Member: ", value="{}".format(str(user)), inline=True)
                embed.add_field(name="Sys ID:", value="`{}`".format(team.ID), inline=True)
                await ctx.send(embed=embed)
            else:
                embed = await utils.create_embed("Team Bracket Assignment Error",
                                                 "Unable to assign Bracket/Allow Checkin")
                await ctx.send(embed=embed)

    @commands.has_role("Staff")
    @commands.command(name='checkinOverride', help="Allows staff to set checkin for teams\n"
                                                   "<checkin>: yes or no to check in/our a team\n"
                                                   "<query>: The team you want to find\n"
                                                   "<queryType>: What to find a team by. Can be ID, teamname or a "
                                                   "mention",
                      aliases=["checkinoverride", "staffcheckin", "staffCheckin"])
    async def staff_checkin(self, ctx, checkin, query, queryType="mention"):
        with ctx.typing():
            activeTournament, discordField, FCField = await self.get_details(str(ctx.message.guild.id))
            if checkin.upper() in ["YES", "TRUE", "YEP"]:
                checkinStatus = True
            else:
                checkinStatus = False
            if queryType.upper() in ["ID", "TEAMID"]:
                teams = await self.database.get_teams(activeTournament, teamID=query)
                checkinReturn = await self.database.set_checkin(checkinStatus, activeTournament, teamID=query)
            elif queryType.upper() in ["NAME", "TEAMNAME"]:
                teams = await self.database.get_teams(activeTournament, teamName=query)
                checkinReturn = await self.database.set_checkin(checkinStatus, activeTournament, teamName=query)
            else:
                username = await self.getUsername(ctx.message.guild.id, query)
                if not username:
                    await ctx.send(embed=await utils.create_embed("Staff Checkin Error",
                                                                  "Invalid Mention"))
                    return
                teams = await self.database.get_teams(activeTournament, captainDiscordUsername=username)
                checkinReturn = await self.database.set_checkin(checkinStatus, activeTournament,
                                                                captainDiscordUsername=username)
            if checkinReturn is None:
                await ctx.send(embed=await utils.create_embed("Staff Checkin Error", "Query found no teams"))
            elif checkinReturn is False:
                await ctx.send(embed=await utils.create_embed("Staff Checkin Error",
                                                              "Query found *more then one* team"))
            elif checkinReturn:
                team = teams[0]
                embed = await utils.create_embed("Staff Checkin", "Checkin Successful!")
                embed.add_field(name="Team Name", value=team.teamName, inline=True)
                embed.add_field(name="Bracket", value=bracketValueDict.get(team.bracket, "Unknown"), inline=True)
                embed.add_field(name="Sys ID:", value="`{}`".format(team.ID), inline=True)
                embed.add_field(name="Battlefy ID:", value="`{}`".format(team.battlefyID), inline=False)
                if team.teamIcon != "Unknown":
                    embed.set_thumbnail(url=team.teamIcon)
                await ctx.send(embed=embed)

    @commands.has_role("Staff")
    @commands.command(name='unassignBracket', help="Remove team from bracket and disable checkin\n"
                                                 "<query>: The team you want to find\n"
                                                 "<queryType>: What to find a team by. Can be ID, teamName or a mention",
                      aliases=["unassignbracket"])
    async def assign_bracket(self, ctx, query, queryType="mention"):
        with ctx.typing():
            activeTournament, discordField, FCField = await self.get_details(str(ctx.message.guild.id))
            if queryType.upper() in ["ID", "TEAMID"]:
                teams = await self.database.get_teams(activeTournament, teamID=query)
            elif queryType.upper() in ["NAME", "TEAMNAME"]:
                teams = await self.database.get_teams(activeTournament, teamName=query)
            else:
                username = await self.getUsername(ctx.message.guild.id, query)
                if not username:
                    await ctx.send(embed=await utils.create_embed("Remove Team From Bracket Error",
                                                                  "Invalid Mention"))
                    return
                teams = await self.database.get_teams(activeTournament, captainDiscordUsername=username)
            if len(teams) > 1 or not teams:
                await ctx.send(embed=await utils.create_embed("Remove Team From Bracket Error",
                                                              "Query returns more/less then one team"))
                return
            team = teams[0]
            if queryType.upper() in ["ID", "TEAMID"]:
                checkinStatus = await self.database.set_allow_checkin(False, activeTournament, teamID=query)
                bracketStatus = await self.database.set_bracket(-1, activeTournament, teamID=query)
            elif queryType.upper() in ["NAME", "TEAMNAME"]:
                checkinStatus = await self.database.set_allow_checkin(False, activeTournament, teamName=query)
                bracketStatus = await self.database.set_bracket(-1, activeTournament, teamName=query)
            else:
                checkinStatus = await self.database.set_allow_checkin(False, activeTournament,
                                                                      captainDiscordUsername=username)
                bracketStatus = await self.database.set_bracket(-1, activeTournament,
                                                                captainDiscordUsername=username)
            if checkinStatus and bracketStatus:
                embed = await utils.create_embed("Remove Team From Bracket", "Bracket Assignment Complete")
                if team.teamIcon != "Unknown":
                    embed.set_thumbnail(url=team.teamIcon)
                embed.add_field(name="Team: ", value=team.teamName, inline=True)
                embed.add_field(name="Sys ID:", value="`{}`".format(team.ID), inline=True)
                await ctx.send(embed=embed)
            else:
                embed = await utils.create_embed("Remove Team From Bracket Error",
                                                 "Unable to remove Bracket/Allow Checkin")
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Teams(bot))
