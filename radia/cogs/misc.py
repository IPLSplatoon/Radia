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

    @commands.command()
    async def scrim(self, ctx):
        """Toggle the scrim role."""
        scrim_role = ctx.guild.get_role(722264366124105809)
        if scrim_role in ctx.author.roles:
            await ctx.author.remove_roles(scrim_role)
            await ctx.message.add_reaction('❎')
        else:
            await ctx.author.add_roles(scrim_role)
            await ctx.message.add_reaction('✅')

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

    @tasks.loop(hours=24)
    async def kraken(self):
        """Remove all of Kraken Mare's roles occasionally."""
        guild = discord.utils.get(self.bot.guilds, id=406137039285649428)
        if guild is None:
            return logging.warning("Cannot run update_roles, is the bot in the correct server?")
        kraken = discord.utils.get(guild.members, id=158733178713014273)
        role_ids = [
            471466333771399168, 563484622717976606, 722500918485975040,
            717481862242762793, 717476155590180876, 717475987821953085,
            406171863698505739, 406160013531283457, 722581040593633364,
            644384378100645910, 724997028291280896, 717475987821953085,
            717476155590180876, 726243712908263484, 726904603756462080,
            726904633720832100, 725146685684056097
        ]
        try:
            await kraken.remove_roles(*[guild.get_role(role_id) for role_id in role_ids])
        except discord.errors.Forbidden:
            logging.warning("Cannot remove kraken's roles, does the bot have the proper permissions?")

    @kraken.before_loop
    async def before_kraken(self):
        await self.bot.wait_until_ready()

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
