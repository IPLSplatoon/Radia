"""Tourney cog."""

import discord
from discord.ext import commands
from typing import List

from radia import utils, battlefy


class Tourney(commands.Cog):
    """Tourney related commands."""

    def __init__(self, bot):
        self.bot = bot
    
    # Agenda Command Group:

    @commands.has_role("Staff")
    @commands.group(invoke_without_command=True, aliases=["calendar", "cal"])
    async def agenda(self, ctx, index: int = None):
        """View the agenda."""
        if index is None:
            await ctx.send(embed=utils.Embed(
                title="🗓️ Agenda",
                description=utils.Embed.list(
                    [item.event.name for item in utils.agenda],
                    ordered=True)
            ))
        else:
            try:
                tourney = utils.agenda.tourney_at(index)
            except IndexError:
                await ctx.send("⛔ **Invalid tournament index**")
            else:
                await ctx.send(embed=utils.Embed(
                    title=f"📅 Event Name: `{tourney.event.name}`",
                    description=self.tourney_desc(ctx, tourney),
                ))

    @agenda.command(aliases=["upcoming"])
    async def next(self, ctx):
        tourney = utils.agenda.next_tourney()
        await ctx.send(embed=utils.Embed(
            title=f"📅 Event Name: `{tourney.event.name}`",
            description=self.tourney_desc(ctx, tourney),
        ))

    @agenda.command(aliases=["previous"])
    async def prev(self, ctx):
        tourney = utils.agenda.prev_tourney()
        await ctx.send(embed=utils.Embed(
            title=f"📆 Event Name: `{tourney.event.name}`",
            description=self.tourney_desc(ctx, tourney),
        ))
    
    @staticmethod
    def tourney_desc(ctx, tourney):
        format_str = 'MMM DD, YYYY h:mm A UTC'
        return "\n".join([
            f"Event Begin Time: `{tourney.event.begin.format(format_str)}`",
            f"Event End Time: `{tourney.event.end.format(format_str)}`",
            f"Battlefy Tournament ID: `{tourney.battlefy}`",
            f"Captain Role: {tourney.get_role(ctx).mention}",
        ])

    # Captain Command Group:

    @commands.has_role("Staff")
    @commands.group(invoke_without_command=True)
    async def captain(self, ctx, index: int = 0):
        """
        Show the current status of captains.
        Group of commands handling the captain roles.
        """
        await ctx.invoke(self.check, index)  # Run 'captain check' command

    @captain.command()
    async def check(self, ctx, index: int = 0, _invalid_captains=None):
        """Show the current status of captains."""
        # Get the tournament teams
        tourney = utils.agenda.tourney_at(index)
        teams: List[battlefy.Team] = await battlefy.connector.get_teams(tourney.battlefy)

        # Create list of invalid captains
        invalid_captains = [
            team for team in teams
            if not await team.captain.get_discord(ctx)
        ] if not _invalid_captains else _invalid_captains
        # Send Status Check
        embed = utils.Embed(
            title=f"🗒️ Captain status check for `{tourney.event.name}`",
            description=f"Invalid Captains / Total Teams: `{len(invalid_captains)}/{len(teams)}`")
        self.embed_invalid_captains(embed, invalid_captains, name="List of invalid captains:")
        await ctx.send(embed=embed)

    @captain.command()
    async def assign(self, ctx, nick: bool = False):
        """Assign captain role to members."""
        tourney = utils.agenda.next_tourney()
        invalid_captains = []
        assigned_to = 0

        # Loop over teams and assign valid captains
        async with ctx.typing():
            teams: List[battlefy.Team] = await battlefy.connector.get_teams(tourney.battlefy)
            for team in teams:
                # Add captain role to members
                try:
                    if (member := await team.captain.get_discord(ctx)) is None:
                        raise discord.DiscordException
                    await member.add_roles(tourney.get_role(ctx))
                    assigned_to += 1
                # Adding role failed, append team to the list of invalid captains
                except discord.DiscordException:
                    invalid_captains.append(team)
                # Adding captain role was successful, edit captain nickname
                else:
                    if nick:
                        await member.edit(nick=team.name[:32])

        # Send Report Embed
        embed = utils.Embed(
            title=f"✅ **Success:** roles assigned for `{tourney.event.name}`",
            description=f"{tourney.get_role(ctx).mention} assigned to `{assigned_to}` members.")
        await ctx.send(embed=embed)
        await ctx.invoke(self.check, 0, invalid_captains)  # Run 'captain check' command

    @captain.command()
    async def remove(self, ctx, index: int = 0, nick: bool = False):
        """Remove captain role from members."""
        tourney = utils.agenda.tourney_at(index)
        removed_from = len(tourney.get_role(ctx).members)

        async with ctx.typing():
            # Loop over members with the captain_role
            for member in tourney.get_role(ctx).members:
                await member.remove_roles(tourney.get_role(ctx))
                if nick:
                    await member.edit(nick=None)

        # Display embed
        embed = utils.Embed(
            title=f"✅ **Success:** roles removed for `{tourney.event.name}`",
            description=f"{tourney.get_role(ctx).mention} removed from `{removed_from}` members.")
        await ctx.send(embed=embed)

    @staticmethod
    def embed_invalid_captains(embed, invalid_captains, **kwargs):
        """Add fields to embed to display number of invalid captains and list their details."""
        embed.add_field(**{
            "value": (
                utils.Embed.list(
                    f"`{team.captain.discord}` | `{team.name}`"
                    for team in invalid_captains)
                if invalid_captains else "> ✨ **~ No invalid captains! ~**"),
            "inline": False,
            **kwargs})


def setup(bot):
    bot.add_cog(Tourney(bot))
