"""Info cog."""

import random

import discord
from discord.ext import commands, tasks

from radia import utils, google


class Info(commands.Cog):
    """Commands that send information to the invoker."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["rule"])
    async def rules(self, ctx, prefix=None, image: bool = False):
        """Send an embedded rules section."""
        if prefix:
            try:
                name, response, image_link = google.connector.rules.get(prefix.lower())
                embed = utils.Embed(title=f"{name.capitalize()} Rules", description=response)
                if image:
                    embed.set_image(image_link)
                await ctx.send(embed=embed)
            except TypeError:
                await ctx.send("Section could not be found, try a different prefix.")
            except google.HollowSheet as e:
                await ctx.send(e)

        else:
            try:
                embed = utils.Embed(title="Rules")
                embed.add_field(
                    name="Options:",
                    value=utils.Embed.list(google.connector.rules.options()))
            except google.HollowSheet as e:
                await ctx.send(e)
            else:
                await ctx.send(embed=embed)

    @commands.command(aliases=["canned"])
    async def whatis(self, ctx, prefix=None, image: bool = False):
        """Send a canned response."""
        if prefix:
            try:
                name, response, image_link = google.connector.whatis.get(prefix.lower())
            except TypeError:
                await ctx.send(self.invalid_whatis(prefix))
            except google.HollowSheet as e:
                await ctx.send(e)
            else:
                embed = utils.Embed(title=f"What Is... {name.capitalize()}?", description=response)
                if image:
                    embed.set_image(url=image_link)
                await ctx.send(embed=embed)
        else:
            try:
                embed = utils.Embed(title="What Is...")
                embed.add_field(
                    name="Options:",
                    value=utils.Embed.list(google.connector.whatis.options()))
            except google.HollowSheet as e:
                await ctx.send(e)
            else:
                await ctx.send(embed=embed)

    def invalid_whatis(self, prefix):
        """Send a random error message when the prefix doesn't exist."""
        return random.choice([
            f"WHAT IS {prefix.upper()}??",
            "Doesn't exist",
            "\*poof*",
            "???",
            "¯\_(ツ)_/¯",
            "a collection of subatomic particles",
        ])


def setup(bot):
    bot.add_cog(Info(bot))
