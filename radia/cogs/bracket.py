"""Bracket cog."""

import logging

import discord
from discord.ext import commands, tasks

from radia import utils


class Bracket(commands.Cog):
    """Manages bracket roles."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def bracket(self, ctx):
        """Group of commands handling the bracket roles."""

    @bracket.command()
    async def remove(self, ctx):
        """Remove the bracket roles from members who currently have it."""
        with ctx.typing():
            # Create list of applicable champion roles
            roles = utils.roles.get(ctx,
                "Alpha",
                "Beta",
                "Gamma"
            )
            # Create a set of all members with any bracket role
            all_champions = set()
            for role in roles:
                all_champions += role.members
            # Remove bracket roles from each of those members
            for member in all_champions:
                await member.remove_roles(*roles)

        # Log all members the bracket roles were removed from
        embed = utils.Embed(
            title="Removed bracket roles from:",
            description=utils.Embed.list_block(f"`{len(all_champions)}` total members."))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Bracket(bot))
