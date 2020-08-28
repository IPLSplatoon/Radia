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
    async def pet(self, ctx):
        """Get a picture of a pet."""
        embed = utils.embed.create(title="Pets!", description="Picture of pets")
        embed.set_image(url=f"https://cdn.vlee.me.uk/TurnipBot/pets/{randint(0, 83)}.png")
        await ctx.send(embed=embed)
    
    @commands.has_role("Staff")
    @commands.command(hidden=True)
    async def alright(self, ctx):
        """Increases one to the counter of people who responded: 'alright'."""
        embed = utils.embed.create(title="alright", description="alright counter: `its_a_stub_lol`")
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['reputation'])
    async def rep(self, ctx, action, mention, *, message):
        """Show your appreciation or disdain for someone."""
        emojis = {
            "+": ["\U0001f44d", "\u2728", "\U0001f389", "\U0001f499", "\U0001f44f", "\U0001f31f"],
            "-": ["\U0001f44e", "\U0001f4a2", "\U0001f52a", "\U0001f52b", "\U0001f611", "\U0001f6ab"]
        }.get(action, False)
        if emojis:
            await ctx.message.add_reaction(choice(emojis))
        else:
            await ctx.send("That's not a valid action")


def setup(bot):
    bot.add_cog(Misc(bot))
