"""Misc cog."""

from random import randint
import discord
from discord.ext import commands

from radia import utils

class Misc(commands.Cog):
    """All the miscellaneous commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['🏓'])
    async def ping(self, ctx):
        embed = discord.Embed(title="🏓 Pong!", description=f"Latency: `{round(self.bot.latency*1000)}ms`", color=0xde2e43)
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def pet(self, ctx):
        """Get a picture of a pet."""
        embed = await utils.embed.create(title="Pets!", description="Picture of pets")
        embed.set_image(url=f"https://cdn.vlee.me.uk/TurnipBot/pets/{randint(0, 83)}.png")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Misc(bot))
