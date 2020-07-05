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
        embed = await utils.embedder.create_embed("Radia Status")
        embed.add_field(name="Version:", value="Alpha 1.0", inline=True)
        embed.add_field(name="Latency:", value="{}ms".format(round(self.bot.latency * 1000, 2)), inline=True)
        embed.add_field(name="Contributors:", value="4", inline=False)
        embed.add_field(name="Powered by Turnip Bot Stack",
                        value="https://github.com/vlee489/Turnip-Bot/", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='pet', help="Get a picture of a pet",
                      pass_context=True, hidden=True)
    async def pet(self, ctx):
        embed = await utils.embedder.create_embed("Pets!", "Picture of pets",
                                                  "https://github.com/vlee489/Turnip-Bot/wiki/Credits")
        ran = numpy.random.randint(0, petPicNumber)
        embed.set_image(url="https://cdn.vlee.me.uk/TurnipBot/pets/{}.png".format(ran))
        await ctx.send(embed=embed)

    @commands.command(name='stream', help="Get Stream Link",
                      pass_context=True, hidden=True)
    async def stream(self, ctx):
        embed = await utils.embedder.create_embed("Stream", "The stream is at @ Inkfarer on Twitch",
                                                  "https://www.twitch.tv/inkfarer")
        await ctx.send(embed=embed)

    @commands.command(name='bracket', help="Get Bracket link",
                      pass_context=True, hidden=True)
    async def bracket(self, ctx):
        embed = await utils.embedder.create_embed("Bracket", "Bracket @ Battlefy.com/low-ink",
                                                  "https://battlefy.com/low-ink/low-ink-june-2020/5ed6c6f60c8581672c929a67/info?infoTab=details")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Other(bot))
