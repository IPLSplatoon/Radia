"""LowInk cog."""

import sys

import discord
from discord.ext import commands

from radia import utils


class LowInk(commands.Cog):
    """Commands specific to Low Ink to handle champion roles, bracket roles and day 2."""

    def __init__(self, bot):
        self.bot = bot

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
                "LI Beta Bracket Champions",
                "LI Gamma Bracket Champions",
                "LI Delta Bracket Champion",
                "LI Epsilon Bracket Champions"
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
