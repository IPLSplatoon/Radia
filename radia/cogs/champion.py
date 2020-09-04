"""Champion cog."""

from discord.ext import commands

from radia import utils


class Champion(commands.Cog):
    """Manages champion roles."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def champion(self, ctx):
        """Group of commands handling the champion roles."""
    
    @champion.command(aliases=["coronate", "crown"])
    async def add(self, ctx, *, mentions):
        """Add the Champion role to members."""
        with ctx.typing():
            # Create list of applicable champion roles
            roles = utils.roles.get(ctx,
                "Past Low Ink Winner",
                "Low Ink Current Champions"
            )
            # Add champion roles from every member mentioned
            for member in ctx.message.mentions:
                await member.add_roles(*roles)
            # Log all members the champion roles were added to
            embed = utils.embed.create(
                title="Added champion roles to:",
                description=utils.embed.list_block(
                    [member.mention for member in ctx.message.mentions]))

        await ctx.send(embed=embed)


    @champion.command(aliases=["dethrone"])
    async def remove(self, ctx):
        """Remove the Champion role from members who currently have it."""
        with ctx.typing():
            # Create list of applicable champion roles
            roles = utils.roles.get(ctx,
                "Low Ink Current Champions",
                "Beta Bracket Champions",
                "Gamma Bracket Champions"
            )
            # Create a list of all members with any champion role
            all_champions = set()
            for role in roles:
                all_champions += role.members
            # Remove champion roles from each of those members
            for member in all_champions:
                await member.remove_roles(*roles)
            # Log all members the champion roles were removed from
            embed = utils.embed.create(
                title="Removed champion roles from:",
                description=utils.embed.list_block(
                    [member.mention for member in all_champions]))

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Champion(bot))
