"""
Contains all commands that give information to users
"""

import gSheetConnector
import utils
from discord.ext import commands, tasks
import discord


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sheets = gSheetConnector.SheetConnector("files/googleAuth.json", "Low Ink Bot DataSet")
        self.rules = self.sheets.get_responses("Rules")
        self.canned = self.sheets.get_responses("Canned Responses")

    @tasks.loop(hours=24)
    async def updates(self):
        self.rules = self.sheets.get_responses("Rules")
        self.canned = self.sheets.get_responses("Canned Responses")

    @commands.has_role("Staff")  # Limits to only staff being able to use command
    @commands.guild_only()
    @commands.command(name='refresh', help="Refresh information")
    async def refresh(self, ctx):
        self.rules = self.sheets.get_responses("Rules")
        self.canned = self.sheets.get_responses("Canned Responses")
        embed = await utils.embedder.create_embed("Refresh", "Responses are now refreshed")
        await ctx.send(embed=embed)

    @commands.command(name='rules', help="Get the rules for Low Ink",
                      aliases=["rule", "Rules", "Rule"])
    async def rules(self, ctx, rules="listAll", image="false"):
        if rules == "listAll":
            embed = await utils.embedder.create_embed("Rules", "List of Rules to view")
            rulesList = await utils.embedder.list_to_code_block(self.rules.options)
            embed.add_field(name="Rule Categories", value=rulesList, inline=False)
            await ctx.send(embed=embed)
        else:
            rules = rules.title()
            if rules in self.rules.variantList:
                reply = self.rules.replies[int(self.rules.variantList[rules])]
                embed = await utils.embedder.create_embed("{} Rules".format(rules), "Rules regarding {}".format(rules))
                embed.add_field(name="Info", value=reply.reply, inline=False)
                if image != "false":
                    embed.set_image(reply.image)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Rule requested is not a valid category! >.<")

    @commands.has_role("Staff")  # Limits to only staff being able to use command
    @commands.guild_only()
    @commands.command(name='whatis', help="Get explanations for Frequently asked questions",
                      aliases=["canned", "whatIs"])
    async def canned(self, ctx, category="listAll", image="false"):
        if category == "listAll":
            embed = await utils.embedder.create_embed("What Is....", "List of What Is.... to view")
            categoryList = await utils.embedder.list_to_code_block(self.canned.options)
            embed.add_field(name="What Is Categories", value=categoryList, inline=False)
            await ctx.send(embed=embed)
        else:
            category = category.title()
            if category in self.canned.variantList:
                reply = self.canned.replies[int(self.canned.variantList[category])]
                embed = await utils.embedder.create_embed("What is {}".format(category),
                                                         "Information on {}".format(category))
                embed.add_field(name="Info", value=reply.reply, inline=False)
                if image != "false":
                    embed.set_image(url=reply.image)
                await ctx.send(embed=embed)
            else:
                await ctx.send("What Is requested is not a valid category! >.<")


def setup(bot):
    bot.add_cog(Information(bot))
