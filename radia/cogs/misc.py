"""Misc cog."""

import logging
from random import randint

import discord
from discord.ext import commands, tasks

from radia import utils


class Misc(commands.Cog):
    """All the miscellaneous commands."""

    def __init__(self, bot):
        self.bot = bot
        self.kraken.start()

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

    @tasks.loop(hours=24)
    async def kraken(self):
        """Remove all of Kraken Mare's roles occasionally."""
        guild = discord.utils.get(self.bot.guilds, id=406137039285649428)
        if guild is None:
            return logging.warning("Cannot run update_roles, is the bot in the Low Ink server?")
        kraken = discord.utils.get(guild.members, id=158733178713014273)
        role_ids = [
            471466333771399168, 563484622717976606, 722500918485975040,
            717481862242762793, 717476155590180876, 717475987821953085,
            406171863698505739, 406160013531283457, 722581040593633364,
            644384378100645910, 724997028291280896, 717475987821953085,
            717476155590180876, 726243712908263484, 726904603756462080,
            726904633720832100, 725146685684056097
        ]
        await kraken.remove_roles(*[guild.get_role(role_id) for role_id in role_ids])

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
