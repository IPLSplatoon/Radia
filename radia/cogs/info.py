"""Info cog."""

import discord
from discord.ext import commands, tasks

from radia import utils, google

class Info(commands.Cog):
    """All of the commands that send the user info."""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def refresh(self, ctx):
        """Reload all the data on the worksheets."""
        await google.connector.rules.refresh()
        await google.connector.canned.refresh()
        await ctx.message.add_reaction("\u2728")

    @commands.command(aliases=["rule"])
    async def rules(self, ctx, prefix=None, image: bool = False):
        if prefix:
            try:
                name, response, image_link = google.connector.rules.get(prefix.lower())
                embed = utils.embed.create(title=f"{name.capitalize()} Rules", description=response)
                if image:
                    embed.set_image(image_link)
                await ctx.send(embed=embed)
            except TypeError:
                await ctx.send("Section could not be found, try a different prefix.")

        else:
            embed = utils.embed.create(title="Rules")
            embed.add_field(
                name="Options:",
                value=utils.embed.listblock(google.connector.rules.options()))
            await ctx.send(embed=embed)

    @commands.command(aliases=["canned"])
    async def whatis(self, ctx, category=None, image: bool = False):
        if category:
            try:
                name, response, image_link = google.connector.whatis.get(category.lower())
                embed = utils.embed.create(title=f"What Is... {name.capitalize()}?", description=response)
                if image:
                    embed.set_image(image_link)
                await ctx.send(embed=embed)
            except TypeError:
                await ctx.send("Section could not be found, try a different category.")

        else:
            embed = utils.embed.create(title="What Is...")
            embed.add_field(
                name="Options:",
                value=utils.embed.listblock(google.connector.whatis.options()))
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
