"""
This Cog Deals directly with all Splatoon related Commands.
"""
import utils
from discord.ext import commands
import discord


class Splatoon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='generateSwiss', help="Generate a swiss map set", aliases=["generateswiss"])
    async def generate_swiss(self, ctx, maps, rounds, bestOf, info=None,
                             modes='Splat Zones,Tower Control,Rainmaker,Clam Blitz'):
        with ctx.typing():
            modes = modes.split(",")
            maps = maps.split(",")
            if not modes or not maps:  # Check that the split has worked correctly
                embed = await utils.create_embed("Generate Swiss Error", "Unable to split Modes/Maps")
                await ctx.send(embed=embed)
                return
            if not rounds.isdigit() or not bestOf.isdigit():  # check rounds and bestOf are given as numbers
                embed = await utils.create_embed("Generate Swiss Error",
                                                 "`Best Of` and/or `rounds` not given as numbers")
                await ctx.send(embed=embed)
                return
            mapsList = await utils.generate_swiss(int(rounds), int(bestOf), maps, modes)
            if mapsList:
                embed = await utils.create_embed("Swiss Map List", info)
                for x in range(len(mapsList)):
                    embed.add_field(name="Round {}".format(x+1), value="```\n{}```".format(mapsList[x]), inline=False)
                await ctx.send(embed=embed)
            else:
                embed = await utils.create_embed("Generate Swiss Error", "Unable generate set")
                await ctx.send(embed=embed)

    @commands.command(name='generateTopCut', help="Generate a swiss map set", aliases=["generatetopcut"])
    async def generate_top_cut(self, ctx, maps, rounds, bestOf, info=None,
                             modes='Splat Zones,Tower Control,Rainmaker,Clam Blitz'):
        with ctx.typing():
            modes = modes.split(",")
            maps = maps.split(",")
            if not modes or not maps:  # Check that the split has worked correctly
                embed = await utils.create_embed("Generate Top Cut Error", "Unable to split Modes/Maps")
                await ctx.send(embed=embed)
                return
            if not rounds.isdigit() or not bestOf.isdigit():  # check rounds and bestOf are given as numbers
                embed = await utils.create_embed("Generate Top Cut Error",
                                                 "`Best Of` and/or `rounds` not given as numbers")
                await ctx.send(embed=embed)
                return
            mapList = await utils.generate_top_cut(int(rounds), int(bestOf), maps, modes)
            if mapList:
                embed = await utils.create_embed("Top Cut Map List", info)
                for x in range(len(mapList)):
                    embed.add_field(name="Round {}".format(x+1), value="```\n{}```".format(mapList[x]), inline=False)
                await ctx.send(embed=embed)
            else:
                embed = await utils.create_embed("Generate Top Cut Error", "Unable generate set")
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Splatoon(bot))
