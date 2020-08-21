"""Misc cog."""

import discord
from discord.ext import commands


class Misc(commands.Cog):
    """All the miscellaneous commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['🏓'])
    async def ping(self, ctx):
        embed = discord.Embed(title="🏓 Pong!", description=f"Latency: `{round(self.bot.latency*1000)}ms`", color=0xde2e43)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Misc(bot))
