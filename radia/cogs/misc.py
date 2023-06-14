"""Misc cog."""

import logging
import random

import discord
from discord.ext import commands, tasks

from radia import utils


class Misc(commands.Cog):
    """Miscellaneous commands."""

    def __init__(self, bot):
        self.bot = bot
        self.kraken.start()
        self.update_presence.start()

    @commands.command(aliases=['🏓'])
    async def ping(self, ctx):
        """Get the latency of the bot."""
        embed = discord.Embed(title="🏓 Pong!", description=f"Latency: `{round(self.bot.latency*1000)}ms`", color=0xde2e43)
        await ctx.send(embed=embed)

    @commands.command()
    async def pet(self, ctx, num: int = None):
        """Get a picture of a pet."""
        embed = utils.Embed(title="Pets!", description="Picture of pets")
        embed.set_image(url=f"https://cdn.vlee.me.uk/TurnipBot/pets/{num if num != None else random.randint(0, 140)}.png")
        await ctx.send(embed=embed)

    @tasks.loop(minutes=1)
    async def update_presence(self):
        """Loop to update the bot presence by selecting one of the strings at random."""
        await self.bot.wait_until_ready()
        await self.bot.change_presence(activity=discord.Game(random.choice([
            "!help to get started",
            # Signup!
            "Signup for Low Ink!",
            "Signup for Swim or Sink!",
            "Signup for Testing Grounds!",
            "Signup for Unnamed Tournament!",
            # funny
            "Powered by High Ink!",
            "Investing in buying LUTI.",
            "Get your coffee grounds 45% off this weekend at Testing Grounds.",
            "Sink or Swim or Swim or Sink",
            "According to all known laws of aviation",
            # Round 4
            "Round 4, here we go again!",
            "The real round 4 were the friends we made along the way.",
            # uwu stuff
            "Sprinkles!",
            "Wawa!",
            # Socials
            "Twitter: @IPLSplatoon",
            "Twitch: twitch.tv/IPLSplatoon",
            "Battlefy: battlefy.com/inkling-performance-labs",
            "Patreon: patreon.com/IPLSplatoon",
            "Github: github.com/IPL-Splat",
            "Youtube: youtube.com/channel/UCFRVQSUskcsB5NjjIZKkWTA",
            "Facebook: facebook.com/IPLSplatoon",
            # People-specific
            "Icon by Ozei!",
            "Ban Kraken Mare",
            "I kid you not Hoeen, he turns himself into a pickle",
            "Go to sleep Lepto",
            "Skye passed out again",
            "Helpdesk needs you .jpg",
        ])))

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Send an unreciprocated error when someone confesses their love for radia.

        This is mainly because of Skye (radia's mine)
        """
        if any(msg in message.content for msg in ["love", "ily"]) and (self.bot.user in message.mentions or "radia" in message.content):
            if message.author.id == 571494333090496514:
                await message.add_reaction("<:radia_uwu:748176810059104358>")
            else:
                await message.channel.send(embed=utils.Embed(title="Error: Unreciprocated"))


def setup(bot):
    bot.add_cog(Misc(bot))
