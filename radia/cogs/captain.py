"""Captain cog."""

from typing import List
import discord
from discord.ext import commands

from radia import utils, battlefy


class Captain(commands.Cog):
    """Manages captain roles."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def captain(self, ctx, *args, **kwargs):
        """
        Show the current status of captains.
        Group of commands handling the captain roles.
        """
        await ctx.invoke(self.check, *args, **kwargs)  # Run 'captain check' command

    @captain.command()
    async def check(self, ctx):
        """Show the current status of captains."""
        # Get the tournament teams
        tourney = utils.agenda.next_tourney()
        teams: List[battlefy.Team] = await battlefy.connector.get_teams(tourney.battlefy)

        # Create list of invalid captains
        invalid_captains = [
            f"{team.captain.discord} | {team.name}"
            for team in teams
            if not await team.captain.get_discord(ctx)
        ]
        # Send Status Check
        embed = utils.Embed(title="Captain Check", description="Here's a quick status check on captains.")
        embed.add_field(name="\ufeff", value="\n".join([
            f"Total Teams: `{len(teams)}`",
            f"Invalid Captains: `{len(invalid_captains)}"
        ]))
        self.embed_invalid_captains(embed, invalid_captains, name="List of invalid captains:")
        await ctx.send(embed=embed)

    @captain.command()
    async def assign(self, ctx, nick: bool = False):
        """Assign captain role to members."""
        tourney = utils.agenda.next_tourney()
        invalid_captains = []
        assigned_to = 0

        # Loop over teams and assign valid captains
        async with ctx.typing():
            teams: List[battlefy.Team] = await battlefy.connector.get_teams(tourney.battlefy)
            for team in teams:
                # Add captain role to members
                try:
                    if (member := await team.captain.get_discord(ctx)) == None:
                        raise discord.DiscordException
                    await member.add_roles(tourney.get_role(ctx))
                    assigned_to += 1
                # Adding role failed, append team to the list of invalid captains
                except discord.DiscordException:
                    invalid_captains.append(f"{team.captain.discord} | {team.name}")
                # Adding captain role was successful, edit captain nickname
                else:
                    if nick:
                        await member.edit(nick=team.name[:32])

        # Send Report Embed
        embed = utils.Embed(
            title=f"✅ **Success:** captain role assigned for {tourney.event.name}",
            description=f"{tourney.get_role(ctx).mention} assigned to `{assigned_to}`")
        self.embed_invalid_captains(embed, invalid_captains)
        await ctx.send(embed=embed)

    @captain.command()
    async def remove(self, ctx, nick: bool = False):
        """Remove captain role from members."""
        tourney = utils.agenda.prev_tourney()

        async with ctx.typing():
            # Loop over members with the captain_role
            for member in tourney.get_role(ctx).members:
                member.remove_roles(tourney.get_role(ctx))
                if nick:
                    await member.edit(nick=None)

        # Display embed
        embed = utils.Embed(
            title=f"✅ **Success:** captain role removed for {tourney.event.name}",
            description=f"{tourney.get_role(ctx).mention} removed from `{len(tourney.get_role(ctx).members)}`")
        await ctx.send(embed=embed)

    @staticmethod
    def embed_invalid_captains(embed, invalid_captains, **kwargs):
        """Add fields to embed to display number of invalid captains and list their details."""
        embed.add_field(
            name="Could not assign the captain role to:",
            value=(
                utils.Embed.list_block(invalid_captains)
                if invalid_captains else "✨ **~ Every captain has their role! ~**"),
            **kwargs)


def setup(bot):
    bot.add_cog(Captain(bot))
