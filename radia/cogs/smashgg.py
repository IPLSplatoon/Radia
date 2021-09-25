""" Smash.gg Cog"""

import discord
from discord.ext import commands
from typing import List

from radia.smashgg.objects import Team
from radia import utils, smashgg


class Smashgg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tournament: smashgg.Tournament = None
        self.event: int = None  # Index of the event in the tournament object

    async def assign_roles(self, ctx: commands.Context, teams: List[Team], role_id: int, all_players: bool = False,
                           remove_old: bool = False):
        role = ctx.guild.get_role(role_id)
        assigned_to = 0
        assigned_list = []

        async with ctx.typing():
            event_teams = teams
            for team in event_teams:
                if all_players:
                    for player in team.players:
                        if member := await player.get_discord(ctx):
                            await member.add_roles(role)
                            assigned_to += 1
                            assigned_list.append(member)
                else:
                    captain = team.captain
                    if captain:
                        if member := await captain.get_discord(ctx):
                            await member.add_roles(role)
                            assigned_to += 1
                            assigned_list.append(member)

        if remove_old:
            for member in role.members:
                if member not in assigned_list:
                    await member.remove_roles(role)

        # Send Report Embed
        embed = utils.Embed(
            title=f"✅ **Success:** roles assigned for `{self.tournament.name}`",
            description=f"{role.mention} assigned to `{assigned_to}` members.")
        await ctx.send(embed=embed)

    @commands.has_role("Staff")
    @commands.group(hidden=True)
    async def smashgg(self, ctx: commands.Context):
        """Group of commands for Smash.gg support"""

    @commands.has_role("Staff")
    @smashgg.command(aliases=["tournament"])
    async def set_tournament(self, ctx: commands.Context, *, tournament_slug: str):
        """Set a tournament using the Smash.gg tournament slug"""
        with ctx.typing():
            tournament = await smashgg.connector.get_tournament(tournament_slug)
            if not tournament:
                return await ctx.send("⛔ **No tournament found**")
            if len(tournament.events) == 1:
                embed = utils.Embed(title=f"Loaded tournament {tournament.name}")
                embed.add_field(name="Event Selected", value=f"{tournament.events[0].name}", inline=False)
                self.tournament = tournament
                self.event = 0
                return await ctx.send(embed=embed)
            return await ctx.send("⛔ **No Support for multi event Tournaments.**")

    @commands.has_role("Staff")
    @smashgg.command()
    async def assign(self, ctx: commands.Context, nick: bool = True, role="887068027068239933"):
        if not self.tournament:
            return await ctx.send("⛔ **No event set**")
        role = ctx.guild.get_role(int(role))
        valid_captains = []
        invalid_captains = []
        assigned_to = 0

        async with ctx.typing():
            event_teams = await self.tournament.events[self.event].get_teams()
            for team in event_teams:
                try:
                    captain = team.captain
                    if not captain:
                        raise discord.DiscordException
                    if (member := await captain.get_discord(ctx)) is None:
                        raise discord.DiscordException
                    await member.add_roles(role)
                    valid_captains.append(member)
                    assigned_to += 1
                except discord.DiscordException:
                    invalid_captains.append(team)
                # Adding captain role was successful, optionally edit captain nickname
                else:
                    if nick:
                        # Attempts to give the name Username-TeamName, if fails, give the teamName limited to 32 char
                        name = f"{team.name} - {member.name}"
                        if len(name) > 32:
                            name = team.name[:32]
                        await member.edit(nick=name)

        # Remove those with the captain role that are not a valid captain
        for member in role.members:
            if member not in valid_captains:
                await member.remove_roles(role)

        # Send Report Embed
        embed = utils.Embed(
            title=f"✅ **Success:** roles assigned for `{self.tournament.name}`",
            description=f"{role.mention} assigned to `{assigned_to}` members.")
        await ctx.send(embed=embed)

        # Send status check embed
        invalid_teams = []
        for team in invalid_captains:
            captain_name = "UNKNOWN"
            captain = team.captain
            if captain:
                captain_name = captain.name
            invalid_teams.append(f"`{captain_name}` | `{team.name}`")
        embed = utils.Embed(
            title=f"🗒️ Captain status check for `{self.tournament.name}`",
            description=f"Invalid Captains / Total Teams: `{len(invalid_teams)}/{len(event_teams)}`")
        embed.add_field(
            name="List of invalid captains:",
            value=utils.Embed.list(invalid_teams) if invalid_teams else "> ✨ **~ No invalid captains! ~**")
        await ctx.send(embed=embed)

    @commands.has_role("Staff")
    @smashgg.command(aliases=['cat'])
    async def category(self, ctx: commands.Context, role="878245267349073980"):
        if not self.tournament:
            return await ctx.send("⛔ **No event set**")
        event_teams = await self.tournament.events[self.event].get_teams()
        await self.assign_roles(ctx, event_teams, int(role), all_players=True)

    @commands.has_role("Staff")
    @smashgg.command()
    async def bracket(self, ctx: commands.Context, bracket, role):
        if not self.tournament:
            return await ctx.send("⛔ **No event set**")
        teams = await self.tournament.events[self.event].get_bracket_teams(bracket)
        await self.assign_roles(ctx, teams, int(role), all_players=True, remove_old=True)

    @commands.has_role("Staff")
    @smashgg.command()
    async def wave(self, ctx: commands.Context, wave, role):
        if not self.tournament:
            return await ctx.send("⛔ **No event set**")
        teams = await self.tournament.events[self.event].get_wave_teams(wave)
        await self.assign_roles(ctx, teams, int(role), all_players=True, remove_old=True)


def setup(bot):
    bot.add_cog(Smashgg(bot))

