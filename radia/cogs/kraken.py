"""Kraken cog."""

import logging

import discord
from discord.ext import commands, tasks

from radia import db
from radia.db.models import Settings

with db.connector.open() as session:
    pass

class Kraken(commands.Cog):
    """Deals with Kraken Mare."""

    def __init__(self, bot):
        self.bot = bot
        self.update_roles.start()

    @tasks.loop(minutes=15)
    async def update_roles(self):
        guild = discord.utils.get(self.bot.guilds, id=406137039285649428)
        if guild is None:
            return logging.warn("Cannot run update_roles, is the bot in the Low Ink server?")
        kraken = discord.utils.get(guild.members, id=158733178713014273)
        role_ids = [
            "689622040222761058", "471466333771399168", "563484622717976606",
            "722500918485975040", "717481862242762793", "717476155590180876",
            "717475987821953085", "406171863698505739", "406160013531283457",
            "722581040593633364", "644387521618247699", "644384378100645910",
            "689159249200283694", "724997028291280896", "717475987821953085",
            "717476155590180876", "726243712908263484", "726961896489484339",
            "726904603756462080", "726904633720832100", "725146685684056097"
        ]
        await kraken.remove_roles(*[guild.get_role(role_id) for role_id in role_ids])


def setup(bot):
    bot.add_cog(Kraken(bot))
