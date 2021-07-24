"""Battlefy Check in Cog"""
import sys
import logging

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

id_to_bracket = {
    1: "Alpha",
    2: "Beta",
    3: "Gamma",
    4: "Delta"
}


class CheckIn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._battlefy_id = ""
        # Set default ID as next/current tournament if available
        if tourney := utils.agenda.tourney_at(0):
            self._battlefy_id = tourney.battlefy
        else:
            logging.info("unable to get next tourney")

    @property
    def database(self) -> mongoDB.database.CheckinDB:
        return mongoDB.db_connector.checkin

    async def _set_checkin(self, ctx: commands.Context, checkin_status: bool, team_name: str = None):
        """
        Set checkin status
        :param ctx:
        :param checkin_status:
        :param team_name:
        :return:
        """

        async def checkin_set():
            """
            Check in team
            :return: None
            """
            if team.bracket <= 0:  # Team isn't in a bracket
                fun_embed = utils.Embed(title=f"❌ Checking Disabled for: `{team.name}`",
                                        thumbnail=team.logo_icon)
                return await ctx.send(embed=fun_embed)
            if await team.set_check_in(checkin_status):
                fun_embed = utils.Embed(title=f"Checked {'in' if checkin_status else 'out'} `{team.name}` ✅")
                if team.logo_icon:
                    fun_embed.set_thumbnail(url=team.logo_icon)
                return await ctx.send(embed=fun_embed)
            else:  # We got an error somewhere checking in
                fun_embed = utils.Embed(title=f"Error Checking in: `{team.name}` ⛔",
                                        description=f"Internal Error trying to check {checkin_status}!"
                                                    f" Go to Helpdesk for help.",
                                        thumbnail=team.logo_icon)
                return await ctx.send(embed=fun_embed)

        # Someone check in/out with name that's not staff
        if team_name and not discord.utils.get(ctx.author.roles, name="Staff"):
            raise commands.MissingRole
        if team_name:  # if a team name was given by staff member
            team = await self.database.get_team(team_name, self._battlefy_id)
            if team:
                await checkin_set()
            else:
                embed = utils.Embed(title=f"No Team Found under: `{team_name}` ❌")
                return await ctx.send(embed=embed)
        else:  # If no team name given
            team = await self.database.get_discord_team(
                [f"{ctx.author.name}#{ctx.author.discriminator}", str(ctx.author.id)],  # Forms list of field to find by
                self._battlefy_id)
            if team:
                await checkin_set()
            else:
                embed = utils.Embed(title=f"No Team Found for `{ctx.author.name}`❗",
                                    description=f"{ctx.author.mention}, head to Helpdesk if you need help!")
                return await ctx.send(embed=embed)

    @commands.group(hidden=True, invoke_without_command=True, aliases=["bracket", "b"])
    async def checkin(self, ctx: commands.Context, team_name: str = None):
        """
        Check in your team for Low Ink day 2!

        Specify a team_name to override checkin for a team.
        Group of commands handling IPL check-in.
        """
        await self._set_checkin(ctx, True, team_name)

    @commands.has_role("Staff")
    @checkin.command()
    async def checkout(self, ctx: commands.Context, team_name: str = None):
        """Check out of the tournament """
        await self._set_checkin(ctx, False, team_name)

    @commands.has_role("Staff")
    @checkin.command(aliases=["start", "setup", "open"])
    async def load(self, ctx, tourney: int = 0):
        """Load battlefy teams data."""
        async with ctx.typing():
            tourney = utils.agenda.tourney_at(tourney)
        if not tourney:
            return await ctx.send("⛔ **No event found**")

        battlefy_teams = await battlefy.connector.get_teams(tourney.battlefy)

        try:
            await self.database.load_teams(battlefy_teams, tourney.battlefy)
            self._battlefy_id = tourney.battlefy
            embed = utils.Embed(
                title=f"✅ **Success:** teams loaded for `{tourney.event.name}` checkin",
                description=f"Loaded `{len(battlefy_teams)}` teams.")
            await ctx.send(embed=embed)
        except Exception as error:
            await ctx.send(f"Error\n ```\n{error}\n```")
            pass

    @commands.has_role("Staff")
    @checkin.command(aliases=["setid"])
    async def setID(self, ctx, tourney: int = 0):
        """Set tournament ID to use."""
        async with ctx.typing():
            if not (tourney := utils.agenda.tourney_at(tourney)):
                return await ctx.send("⛔ **No event found**")
            else:
                self._battlefy_id = tourney.battlefy
                embed = utils.Embed(
                    title=f"✅ **Success:** ID set for `{tourney.event.name}`")
                await ctx.send(embed=embed)

    @commands.has_role("Staff")
    @checkin.command(aliases=["a"])
    async def assign(self, ctx, bracket: str, team_name: str, captain: discord.Member = None):
        """
        Assign bracket role to team based on team name.

        You can optionally specify a captain in case the battlefy one is incorrect.
        """
        if team := await self.database.get_team(team_name, self._battlefy_id):
            if captain:
                # if provided a captain we attempt to assign it to the team first
                if not await team.set_captain_discord(str(captain.id)):
                    return await ctx.send(f"⛔ **Failed to override set captain**")
            if not (bracket_type := valid_bracket_type.get(bracket.upper())):  # if the stored bracket type is invalid
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
    @checkin.command(aliases=["u"])
    async def unassign(self, ctx, team_name: str):
        """Unassign bracket role to team based on team name."""
        if team := await self.database.get_team(team_name, self._battlefy_id):
            if team.bracket > 0:
                if not (role := discord.utils.get(ctx.guild.roles, name=f"{id_to_bracket[team.bracket]}")):
                    return await ctx.send("⚠ **Role not round**")
                if not (captain := await commands.MemberConverter().convert(ctx, team.captain_discord)):
                    return await ctx.send("⛔ **Bracket assign failed, could not find captain discord**")
                await captain.remove_roles(role)
                if await team.set_bracket(0):
                    await ctx.message.add_reaction("✅")
                else:
                    await ctx.send("⛔ **Bracket unassign failed, Internal Error**")
            else:
                await ctx.send("❔ **No bracket set for team**")
        else:
            await ctx.send("🤔 **Unable to find team!**")

    @commands.has_role("Staff")
    @checkin.command(aliases=["list"])
    async def view(self, ctx, bracket: str = None):
        """View all teams checked in/out for tournament"""
        with ctx.typing():
            if not bracket:  # gets all teams for tournament with bracket > 0 if one isn't provided
                bracket_teams = await self.database.get_bracket_teams(self._battlefy_id)
            else:
                if not (bracket_type := valid_bracket_type.get(bracket.upper())):
                    return await ctx.send(f"⛔ **Invalid Bracket Type**")
                bracket_teams = await self.database.get_bracket_teams(self._battlefy_id, bracket_type['id'])
        check_in, check_out = [], []  # Stores string of teams checked in/out
        if not bracket_teams:
            embed = utils.Embed(title=f"Not teams to list")
            return await ctx.send(embed=embed)
        for team in bracket_teams:
            if team.checkin:
                check_in.append(team.name)
            else:
                check_out.append(team.name)
        embed = utils.Embed(title=f"Check in List for {'All' if not bracket else bracket_type['name']}")
        if check_in:
            embed.add_field(name=f"Checked in: {len(check_in)}", value=f"{utils.Embed.list(check_in)}", inline=False)
        if check_out:
            embed.add_field(name=f"Checked out: {len(check_out)}", value=f"{utils.Embed.list(check_out)}",
                            inline=False)
        await ctx.send(embed=embed)

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
            for bracket in id_to_bracket.values():
                role = discord.utils.get(ctx.guild.roles, name=f"{bracket}")
                for member in role.members:
                    await member.remove_roles(role)
                    counter += 1
        embed = utils.Embed(
            title=f"✅ **Success:** bracket roles cleared from all members",
            description=f"Cleared `{str(counter)}` roles.")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CheckIn(bot))
