"""
Deals with random commands
"""
import utils
from discord.ext import commands
import numpy

petPicNumber = 65


class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='stats', help="Gets the stats for the bot")
    async def stats(self, ctx):
        embed = await utils.embeder.create_embed("Radia Status")
        embed.add_field(name="Version:", value="Alpha 1.0", inline=True)
        embed.add_field(name="Latency:", value="{}ms".format(round(self.bot.latency * 1000, 2)), inline=True)
        embed.add_field(name="Contributors:", value="1", inline=False)
        embed.add_field(name="Powered by Turnip Bot Stack",
                        value="https://github.com/vlee489/Turnip-Bot/", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='pet', help="Get a picture of a pet",
                      pass_context=True, hidden=False)
    async def pet(self, ctx):
        embed = await utils.embeder.create_embed("Pets!", "Picture of pets",
                                                 "https://github.com/vlee489/Turnip-Bot/wiki/Credits")
        ran = numpy.random.randint(0, petPicNumber)
        embed.set_image(url="https://cdn.vlee.me.uk/TurnipBot/pets/{}.png".format(ran))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Other(bot))
