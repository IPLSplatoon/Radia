"""LowInk cog."""

import sys

import discord
from discord.ext import commands
from discord.ext.commands import Context

from radia import utils, battlefy, mongoDB


class LowInk(commands.Cog):
    """Commands specific to Low Ink to handle champion roles, bracket roles and day 2."""

    def __init__(self, bot):
        self.bot = bot
        self.battlefy_teams = []
        self.checkedin_teams = []

    # Checkin

    @commands.group(hidden=True, invoke_without_command=True, aliases=["bracket", "b"])
    async def checkin(self, ctx, team_name: str = None):
        """ Check in your team for Low Ink day 2!

        Specify a team_name to override checkin for a team.
        Group of commands handling Low Ink day 2 check-in.
        """
        if team_name and not discord.utils.get(ctx.author.roles, name="Staff"):
            raise commands.MissingRole

        for team in self.battlefy_teams:
            # Check if team is allowed to check in
            if await team.get_bracket(ctx):
                if all([  # No team_name provided, check if captain discord == author discord
                    not team_name,
                    getattr(await team.captain.get_discord(ctx), "id", None) == ctx.author.id,
                ]) or all([  # team_name provided, check if the team names match
                    team_name,
                    team.name == team_name,
                ]):
                    if team in self.checkedin_teams:
                        return await ctx.send("⛔ **Check-in failed, you're already checked in!**")
                    self.checkedin_teams.append(team)
                    await ctx.message.add_reaction("✅")
                    break
        else:
            await ctx.send("⛔ **Check-in failed, unable to find team**")

    @commands.has_role("Staff")
    @checkin.command(aliases=["start", "setup", "open"])
    async def load(self, ctx, tourney: int = 0):
        """Load battlefy teams data."""
        async with ctx.typing():
            tourney = utils.agenda.tourney_at(tourney)
        if not tourney:
            return await ctx.send("⛔ **No event found**")

        self.battlefy_teams = await battlefy.connector.get_teams(tourney.battlefy)
        self.checkedin_teams = []
        embed = utils.Embed(
            title=f"✅ **Success:** teams loaded for `{tourney.event.name}` checkin",
            description=f"Loaded `{len(self.battlefy_teams)}` teams.")
        await ctx.send(embed=embed)

    @commands.has_role("Staff")
    @checkin.command(aliases=["a"])
    async def assign(self, ctx, bracket, team_name, captain: discord.Member = None):
        """Assign bracket role to team based on team name.

        You can optionally specify a captain in case the battlefy one is incorrect.
        """
        for team in self.battlefy_teams:
            if team.name == team_name:
                if captain:
                    team.captain = team.captain.__class__(
                        battlefy=team.captain.raw,
                        fc_field=team.captain.fc,
                        discord_field=str(captain.id))
                try:
                    await team.assign_bracket(ctx, bracket)
                except ValueError as e:
                    await ctx.send(f"⛔ **Bracket assign failed, {e}**")
                except commands.BadArgument:
                    await ctx.send("⛔ **Bracket assign failed, could not find captain discord**")
                else:
                    await ctx.message.add_reaction("✅")
                break
        else:
            await ctx.send("⛔ **Bracket assign failed, unable to find team**")

    @commands.has_role("Staff")
    @checkin.command(aliases=["list"])
    async def view(self, ctx, bracket: str = None):
        """List all of the teams that have checked in."""
        display_list = []
        if bracket:
            bracket = battlefy.Team.Bracket.find(bracket)
        else:
            bracket = None
        async with ctx.typing():
            for team in self.checkedin_teams:
                captain_mention = getattr(await team.captain.get_discord(ctx), 'mention', None)
                team_bracket = await team.get_bracket(ctx)
                if bracket:
                    if bracket != "false" and team_bracket != bracket:
                        continue
                    elif bracket == "false" and team_bracket != None:
                        continue
                display_list.append(f"`{team_bracket.value}` `{team.name}` {captain_mention}")
        await ctx.send(embed=utils.Embed(
            title=f"Checked-in teams for {bracket.name.capitalize() if bracket else 'all brackets'}",
            description=utils.Embed.list(display_list)
        ))

    @commands.has_role("Staff")
    @checkin.command(aliases=["remove"])
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

    @commands.has_role("Staff")
    @checkin.command(aliases=["clean"])
    async def purge(self, ctx):
        """Purge the current check-in channel of messages, and clear the list of checked in players."""
        if 'check-in' in ctx.channel.name:
            await ctx.channel.purge(limit=sys.maxsize)
        else:
            await ctx.channel.send("⛔ **You'd better be careful throwing that command around**")

    # Champion

    @commands.has_role("Staff")
    @commands.group(hidden=True)
    async def champion(self, ctx):
        """Group of commands handling the champion roles."""

    @commands.has_role("Staff")
    @champion.command(aliases=["coronate", "crown"])
    async def add(self, ctx):
        """Add the Champion role to members."""
        with ctx.typing():
            # Create list of applicable champion roles
            roles = self.get_roles(ctx,
                "Past Low Ink Winner",
                "Low Ink Current Champions"
            )
            # Add champion roles from every member mentioned
            for member in ctx.message.mentions:
                await member.add_roles(*roles)

        # Log all members the champion roles were added to
        embed = utils.Embed(
            title="Added champion roles to:",
            description=utils.Embed.list(
                [member.mention for member in ctx.message.mentions]))
        await ctx.send(embed=embed)

    @commands.has_role("Staff")
    @champion.command(aliases=["dethrone"])
    async def remove(self, ctx):
        """Remove the champion roles from members who currently have it."""
        with ctx.typing():
            # Create list of applicable champion roles
            roles = self.get_roles(ctx,
                "Low Ink Current Champions",
                "Beta Bracket Champions",
                "Gamma Bracket Champions"
            )
            # Create a set of all members with any champion role
            all_champions = list()
            for role in roles:
                all_champions += role.members
            # Remove champion roles from each of those members
            for member in all_champions:
                await member.remove_roles(*roles)

        # Log all members the champion roles were removed from
        embed = utils.Embed(
            title="Removed champion roles from:",
            description=utils.Embed.list(
                [member.mention for member in all_champions]))
        await ctx.send(embed=embed)

    # Utils

    @staticmethod
    def get_roles(ctx, *names):
        """Get a list of all the roles with the given role names."""
        return [
            role
            for name in names
            if (role := discord.utils.get(ctx.guild.roles, name=name))
        ]


def setup(bot):
    bot.add_cog(LowInk(bot))
