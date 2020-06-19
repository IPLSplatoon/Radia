"""
Deals with Kraken Mare
"""

import utils
from discord.ext import commands, tasks
import discord


class Kraken(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_roles.start()

    @tasks.loop(minutes=15)
    async def update_roles(self):
        for guild in self.bot.guilds:
            if guild.id == 406137039285649428:
                KrakenMare = discord.utils.get(guild.members, id=158733178713014273)  # Gets kraken Mare object
                toRemove = [
                    "689622040222761058",
                    "471466333771399168",
                    "563484622717976606",
                    "722500918485975040",
                    "717481862242762793",
                    "717476155590180876",
                    "717475987821953085",
                    "406171863698505739",
                    "406160013531283457",
                    "722581040593633364",
                    "644387521618247699",
                    "644384378100645910",
                    "689159249200283694"
                ]

                for role in KrakenMare.roles:
                    if str(role.id) in toRemove:
                        await KrakenMare.remove_roles(role)

def setup(bot):
    bot.add_cog(Kraken(bot))
