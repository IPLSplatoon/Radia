"""
This Cog Deals directly with all Splatoon related Commands.
"""
from discord.ext import commands
from mapListGen import MapToolkit
from utils import embedder


class Splatoon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mapGen = MapToolkit("files/mapDB.pickle")

    @commands.command(name="setMapList", help="Set map list\n"
                                              "<sz>: List of splat zones maps, seperated by commas.\n"
                                              "<tc>: List of tower control maps, seperated by commas.\n"
                                              "<rm>: List of rainmaker maps, seperated by commas.\n"
                                              "<cb>: List of clam blitz maps, seperated by commas.\n")
    async def set_map_list(self, ctx, sz, tc, rm, cb):
        with ctx.typing():
            response = await self.mapGen.setMaps(sz, tc, rm, cb)
            if response:
                await ctx.send(embed=await embedder.create_embed("Set Map", "Maps set"))
            else:
                await ctx.send(embed=
                               await embedder.create_embed("Set Map Error",
                                                           "Not Enough maps provided for one/more modes"))

    @commands.command(name="setBracket", help="Set the bracket\n"
                                              "<bracket>: Bracket and best of in the format\n"
                                              "\"Bracket count, best of, Bracket count, best of...........\"\n"
                                              "Separating each with commas")
    async def set_brackets(self, ctx, bracket):
        with ctx.typing():
            response = await self.mapGen.setBrackets(bracket)
            if response:
                await ctx.send(embed=await embedder.create_embed("Set Bracket", "Bracket format set"))
            else:
                await ctx.send(embed=await embedder.create_embed("Set Bracket Error", "Bracket not in pairs!"))

    @commands.command(name="generateSet", help="Generate a set\n"
                                               "<seed>: Seed to generate bracket with\n")
    async def generate_set(self, ctx, seed):
        with ctx.typing():
            response = await self.mapGen.generateBracket(seed)
            if response:
                await ctx.send(embed=response)
            else:
                await ctx.send(embed=await embedder.create_embed("Generate Set Error",
                                                                 "Bracket/Set data blank and/or generator is locked"))

    @commands.command(name="getSet", help="Get an already existing set\n"
                                          "<seed>: Seed to generate bracket with\n")
    async def get_set(self, ctx):
        with ctx.typing():
            response = await self.mapGen.getBracket()
            if response:
                await ctx.send(embed=response)
            else:
                await ctx.send(embed=await embedder.create_embed("Get Set Error", "Set data doesn't exist"))

    @commands.command(name="getSettings", help="Get settings in storage\n")
    async def get_settings(self, ctx):
        with ctx.typing():
            await ctx.send(embed=await self.mapGen.getSettings())

    @commands.command(name="toggleLock", help="Toggle Lock for det Generator\n")
    async def toggle_lock(self, ctx):
        with ctx.typing():
            response = await self.mapGen.toggleLock()
            embed = await embedder.create_embed("Toggle Lock")
            if response:
                embed.add_field(name="Lock State:", value="**On**", inline=False)
            else:
                embed.add_field(name="Lock State:", value="**Off**", inline=False)
            await ctx.send(embed=embed)

    @commands.command(name="getJSON", help="Get set in JSON format")
    async def get_JSON(self, ctx):
        with ctx.typing():
            response = await self.mapGen.uploadJSON()
            if response is None:
                await ctx.send(embed=await embedder.create_embed("Get Set Error", "Set data doesn't exist"))
            else:
                embed = await embedder.create_embed("JSON Download", "JSON Uploaded", response)
                embed.add_field(name="Link:", value="`{}`".format(response), inline=False)
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Splatoon(bot))
