"""Battlefy Check in Cog"""
import sys

import discord
from discord.ext import commands

from radia import utils, battlefy, mongoDB

valid_bracket_type = {
    "A": {"name": "Alpha", "id": 1},
    "B": {"name": "Beta", "id": 2},
    "G": {"name": "Gamma", "id": 3},
    "D": {"name": "Delta", "id": 4},
    "ALPHA": {"name": "Alpha", "id": 1},
    "BETA": {"name": "Beta", "id": 2},
    "GAMMA": {"name": "Gamma", "id": 3},
    "DELTA": {"name": "Delta", "id": 4}
}


class CheckIn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._battlefy_id = utils.agenda.tourney_at(0).battlefy  # Set default ID as next/current tournament

    @property
    def database(self) -> mongoDB.database.CheckinDB:
        return mongoDB.db_connector.checkin

    @commands.group(hidden=True, invoke_without_command=True, aliases=["bracket", "b"])
    async def checkin(self, ctx: commands.Context, team_name: str = None):
        """ Check in your team for Low Ink day 2!

        Specify a team_name to override checkin for a team.
        Group of commands handling Low Ink day 2 check-in.
        """
        async def checkin(team_object: mongoDB.MongoTeam):
            """
            Check in team
            :param team_object: Team to check in
            :return: None
            """
            if team_object.bracket <= 0:
                embed = utils.Embed(title=f"❌ Checking Disabled for {team_object.name}",
                                    thumbnail=team.logo_icon)
                return await ctx.send(embed=embed)
            if await team_object.set_check_in(True):
                embed = utils.Embed(title=f"Checked in {team.name} ✅",
                                    thumbnail=team.logo_icon)
                return await ctx.send(embed=embed)
            else:
                embed = utils.Embed(title=f"Error Checking in {team.name} ⛔",
                                    description="Internal Error trying to check in! Go to Helpdesk for help.",
                                    thumbnail=team.logo_icon)
                return await ctx.send(embed=embed)

        if team_name and not discord.utils.get(ctx.author.roles, name="Staff"):
            raise commands.MissingRole
        if team_name:
            team = await self.database.get_team(team_name, self._battlefy_id)
            if team:
                await checkin(team)
            else:
                embed = utils.Embed(title=f"No Team Found under {team_name} ❌")
                return await ctx.send(embed=embed)
        else:
            team = await self.database.get_discord_team(
                [f"{ctx.author.name}#{ctx.author.discriminator}", str(ctx.author.id)],  # Forms list of field to find by
                self._battlefy_id)
            if team:
                await checkin(team)
            else:
                embed = utils.Embed(title=f"No Team Found for {ctx.author.mention}❗",
                                    description="Head to Helpdesk if you need help!")
                return await ctx.send(embed=embed)


    @commands.has_role("Staff")
    @checkin.command(aliases=["start", "setup", "open"])
    async def load(self, ctx, tourney: int = 0):
        """Load battlefy teams data."""
        async with ctx.typing():
            tourney = utils.agenda.tourney_at(tourney)
        if not tourney:
            return await ctx.send("⛔ **No event found**")

        battlefy_teams = await battlefy.connector.get_teams(tourney.battlefy)

        # try:
        await mongoDB.db_connector.checkin.load_teams(battlefy_teams, tourney.battlefy)
        self._battlefy_id = tourney.battlefy
        embed = utils.Embed(
            title=f"✅ **Success:** teams loaded for `{tourney.event.name}` checkin",
            description=f"Loaded `{len(battlefy_teams)}` teams.")
        await ctx.send(embed=embed)
        # except Exception as error:
        #     await ctx.send(f"Error\n ```\n{error}\n```")
        #     pass

    @commands.has_role("Staff")
    @checkin.command(aliases=["a"])
    async def assign(self, ctx, bracket: str, team_name: str, captain: discord.Member = None):
        """Assign bracket role to team based on team name.

        You can optionally specify a captain in case the battlefy one is incorrect.
        """
        team = await self.database.get_team(team_name, self._battlefy_id)
        if team:
            if captain:
                if not await team.set_captain_discord(str(captain.id)):
                    return await ctx.send(f"⛔ **Failed to override set captain**")
            if not (bracket_type := valid_bracket_type.get(bracket.upper())):
                return await ctx.send(f"⛔ **Invalid Bracket Type**")
            try:
                if await team.set_assign_bracket(ctx, bracket_type):
                    await ctx.message.add_reaction("✅")
                else:
                    await ctx.send("⛔ **Bracket assign failed, Internal Error**")
            except mongoDB.CaptainNotFound:
                await ctx.send("⛔ **Bracket assign failed, could not find captain discord**")
            except discord.Forbidden:
                await ctx.send("⛔ **Insufficient Permissions to set Role**")
        else:
            await ctx.send("🤔 **Unable to find team!**")

    @commands.has_role("Staff")
    @checkin.command(aliases=["clean"])
    async def purge(self, ctx):
        """Purge the current check-in channel of messages, and clear the list of checked in players."""
        if 'check-in' in ctx.channel.name:
            await ctx.channel.purge(limit=sys.maxsize)
        else:
            await ctx.channel.send("⛔ **You'd better be careful throwing that command around**")

    @commands.has_role("Staff")
    @checkin.command()
    async def clear(self, ctx):
        """Remove all of the bracket roles."""
        async with ctx.typing():
            counter = 0
            for bracket in battlefy.Team.Bracket:
                bracket_role = bracket.role(ctx)
                for member in bracket_role.members:
                    await member.remove_roles(bracket_role)
                    counter += 1
        embed = utils.Embed(
            title=f"✅ **Success:** bracket roles cleared from all members",
            description=f"Cleared `{str(counter)}` roles.")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CheckIn(bot))
