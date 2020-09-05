"""Captain cog."""

import discord
from discord.ext import commands

from radia import utils, battlefy#, db


class Captain(commands.Cog):
    """Manages captain roles."""

    def __init__(self, bot):
        self.bot = bot
        self.member = commands.MemberConverter()

    @commands.group(invoke_without_subcommand=True)
    async def captain(self, ctx, *args, **kwargs):
        """
        Show the current status of captains.
        Group of commands handling the captain roles.
        """
        await ctx.invoke(self.check, *args, **kwargs)  # Run 'captain check' command

    @captain.command()
    async def check(self, ctx):
        """Show the current status of captains."""
        # settings = db.connector.find_settings(server=ctx.guild.id)
        teams = await battlefy.connector.get_teams("5f21e5e1f5fc96423c53d094") # DB: settings.tournament

        # Create list of invalid captains
        invalid_captains = [
            f"{team.captain.discord} | {team.name}"
            for team in teams
            if not await self.in_server(ctx, team.captain.discord)
        ]
        # Send Status Check
        embed = utils.embed.create(title="Captain Check", description="Here's a quick status check on captains.")
        embed.add_field(name="\ufeff", value="\n".join([
            f"Total Teams: `{len(teams)}`",
            f"Invalid Captains: `{len(invalid_captains)}"
        ]))
        if invalid_captains:  # Create a field to list the invalid captains, if there are any
            embed.add_field(name="List of Invalid Captains:", value=utils.embed.list_block(invalid_captains))
        await ctx.send(embed=embed)

    @captain.command()
    async def assign(self, ctx):
        pass

    @captain.command()
    async def remove(self, ctx, nick: bool = False):
        """Remove captain role from members."""
        # settings = db.connector.find_settings(server=ctx.guild.id)
        captain_role = ctx.guild.get_role("406171863698505739")  # DB: settings.captain_role
        
        with ctx.typing():
            # Loop over members with the captain_role
            for member in captain_role.members:
                member.remove_roles(captain_role)
                if nick:
                    await member.edit(nick=None)

            # Display embed
            embed = await utils.embed.create(
                title="Success: Captain Role Removed",
                description=f"Removed Captain role from `{len(captain_role.members)}` members.")
        await ctx.send(embed=embed)

    async def in_server(self, ctx, member: str) -> bool:
        """Check if any string representation of a member is in the server or not."""
        try:
            await self.member.convert(ctx, member)
        except commands.BadArgument:
            return False
        return True


def setup(bot):
    bot.add_cog(Captain(bot))
