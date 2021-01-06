"""Agenda cog."""

import discord
from discord.ext import commands

from radia import utils


class Agenda(commands.Cog):
    """Agenda related commands."""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.has_role("Staff")
    @commands.group(invoke_without_command=True)
    async def agenda(self, ctx, index: int = None):
        """View the agenda."""
        if index is None:
            await ctx.send(embed=utils.Embed(
                title="📅 Agenda",
                description="\n".join([
                    f"`{index}:` {item.event.name}"
                    for index, item in enumerate(utils.agenda)])
            ))
        else:
            try:
                tourney = list(utils.agenda)[index]
            except IndexError:
                await ctx.send("⛔ **Invalid tournament index**")
            else:
                await ctx.send(embed=utils.Embed(
                    title="Upcoming Tournament",
                    description=self.tourney_desc(ctx, tourney),
                ))

    @agenda.command(aliases=["upcoming"])
    async def next(self, ctx):
        tourney = utils.agenda.next_tourney()
        await ctx.send(embed=utils.Embed(
            title="Upcoming Tournament",
            description=self.tourney_desc(ctx, tourney),
        ))

    @agenda.command(aliases=["previous"])
    async def prev(self, ctx):
        tourney = utils.agenda.prev_tourney()
        await ctx.send(embed=utils.Embed(
            title="Previous Tournament",
            description=self.tourney_desc(ctx, tourney),
        ))
    
    @staticmethod
    def tourney_desc(ctx, tourney):
        format_str = 'MMM DD, YYYY h:mm A UTC'
        return "\n".join([
            f"Name: `{tourney.event.name}`",
            f"Starting Time: `{tourney.event.begin.format(format_str)}`",
            f"Ending Time: `{tourney.event.end.format(format_str)}`",
            f"Battlefy Tournament ID: `{tourney.battlefy}`",
            f"Captain Role: {tourney.get_role(ctx).mention}",
        ])

def setup(bot):
    bot.add_cog(Agenda(bot))
