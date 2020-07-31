"""
This Cog Deals directly with all Splatoon related Commands.
"""
from discord.ext import commands
import discord
import time
import utils


class Splatoon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="generateMapList", help="Generate a Map List\n"
                                                   "<sz>: List of splat zones maps, seperated by commas.\n"
                                                   "<tc>: List of tower control maps, seperated by commas.\n"
                                                   "<rm>: List of rainmaker maps, seperated by commas.\n"
                                                   "<cb>: List of clam blitz maps, seperated by commas.\n"
                                                   "(Remainder) <brackets>: List each bracket as such \"(num rounds),(num games)\"")
    async def generate_maps_comm(ctx, sz:str, tc:str, rm:str, cb:str, *brackets):
        #attempt to create a map pool from the user inputs
        built_map_pool = utils.build_map_pool(sz,tc,rm,cb)
        if type(built_map_pool) is str:
            await ctx.send(built_map_pool)
            return

        #attempt to create a bracket list from the user inputs
        built_brackets = utils.build_brackets(brackets)
        if type(built_brackets) is str:
            await ctx.send(built_brackets)
            return

        #Generate a seed
        seed = time.time()

        #Generate map list
        map_list = utils.generate_maps(built_map_pool, built_brackets, seed)

        #Generate embed
        embed = utils.get_map_list_embed(map_list)

        #TODO: Vincent, save the built_map_pool, seed, and built_brackets variables into the database. Thats all the info needed to regenerate a map list.

        await ctx.send(embed=embed)

    @commands.command(name='setCurrentMapList')
    async def set_current_map_list(ctx):
        #TODO: This command should save the latest generated map list so it won't be overwritten
        return


    @commands.command(name="currentMapList")
    async def current_map_list(ctx):
        map_pool = [] #TODO: Get the saved map pool from the database
        brackets = [] #TODO: Get the bracket data from the database
        seed = 0 #TODO: Get the saved map seed from the database

        map_list = utils.generate_maps(map_pool, brackets, seed)

        embed = utils.get_map_list_embed(map_list)
        await ctx.send(embed=embed)

    @commands.command(name="currentMapListJson")
    async def current_map_list_json(ctx):
        map_pool = []#TODO: Get the saved map pool from the database
        brackets = [] #TODO: Get the bracket data from the database
        seed = 0 #TODO: Get the saved map seed from the database

        map_list = utils.generate_maps(map_pool, brackets, seed)

        json = utils.get_map_list_json(map_list)
        await ctx.send("```json\n{0}```".format(json))
        #TODO: Maybe make this upload a file instead


def setup(bot):
    bot.add_cog(Splatoon(bot))
