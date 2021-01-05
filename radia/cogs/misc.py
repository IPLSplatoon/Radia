"""Misc cog."""

from random import choice, randint

import discord
from discord.ext import commands

from radia import utils


class Misc(commands.Cog):
    """All the miscellaneous commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['🏓'])
    async def ping(self, ctx):
        """Get the latency of the bot."""
        embed = discord.Embed(title="🏓 Pong!", description=f"Latency: `{round(self.bot.latency*1000)}ms`", color=0xde2e43)
        await ctx.send(embed=embed)

    @commands.command()
    async def pet(self, ctx, num: int = None):
        """Get a picture of a pet."""
        embed = utils.Embed(title="Pets!", description="Picture of pets")
        embed.set_image(url=f"https://cdn.vlee.me.uk/TurnipBot/pets/{num if num != None else randint(0, 83)}.png")
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Send an unreciprocated error when someone confesses their love for radia.

        This is mainly because of Skye (radia's mine)
        """
        if any(msg in message.content for msg in ["love", "ily"]) and (self.bot.user in message.mentions or "radia" in message.content):
            await message.channel.send(embed=utils.Embed(title="Error: Unreciprocated"))


def setup(bot):
    bot.add_cog(Misc(bot))
