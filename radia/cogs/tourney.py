"""Tourney cog."""

import json
from io import BytesIO

import discord
from discord.ext import commands

from radia import utils, battlefy, sendouConnector


class Tourney(commands.Cog, command_attrs={"hidden": True}):
    """ Commands for staff members to manage upcoming and ongoing tournaments.

    - View dates and ordering of tournament events with the agenda commands.
    - Manage assigning and removing of the captain role for tournaments with the captain commands.
    """

    def __init__(self, bot):
        self.bot = bot
        self.sendou = sendouConnector.Connector()

    # Agenda Command Group:

    @commands.has_role("Staff")
    @commands.group(invoke_without_command=True, aliases=["calendar", "cal"])
    async def agenda(self, ctx, index: int = None):
        """View the agenda."""
        if index is None:
            # Send an embedded list of all of the agenda events
            await ctx.send(embed=utils.Embed(
                title="🗓️ Agenda",
                description=utils.Embed.list(
                    [item.event.name for item in utils.agenda],
                    ordered=True)
            ))
        else:
            # Send an embed of the event at index, send an error if it fails
            tourney = utils.agenda.tourney_at(index)
            if not tourney:
                await ctx.send("⛔ **No event found**")
            else:
                await ctx.send(embed=utils.Embed(
                    title=f"📅 Event Name: `{tourney.event.name}`",
                    description=self.tourney_desc(ctx, tourney)))

    @commands.has_role("Staff")
    @agenda.command(aliases=["upcoming"])
    async def next(self, ctx):
        tourney = utils.agenda.next_tourney()
        if not tourney:
            return await ctx.send("⛔ **No event found**")
        await ctx.send(embed=utils.Embed(
            title=f"📅 Event Name: `{tourney.event.name}`",
            description=self.tourney_desc(ctx, tourney),
        ))

    @commands.has_role("Staff")
    @agenda.command(aliases=["previous"])
    async def prev(self, ctx):
        tourney = utils.agenda.prev_tourney()
        if not tourney:
            return await ctx.send("⛔ **No event found**")
        await ctx.send(embed=utils.Embed(
            title=f"📆 Event Name: `{tourney.event.name}`",
            description=self.tourney_desc(ctx, tourney),
        ))

    @commands.has_role("Staff")
    @agenda.command(aliases=["download"])
    async def export(self, ctx, index: int = 0):
        """Freeze and download a compiled report of the team data for a tournament."""
        tourney = utils.agenda.tourney_at(index)
        if not tourney:
            return await ctx.send("⛔ **No event found**")
        async with ctx.typing():
            battlefy_tourney = await battlefy.connector.get_tournament(tourney.battlefy)
            # Build exported data dictionary, to dump to json file
            exported_data = {
                "name": tourney.event.name,
                "role": tourney.role,
                "battlefy": battlefy_tourney.raw,
                "start_time": str(battlefy_tourney.start_time),
                "teams": [
                    {
                        "raw": team.raw,
                        "name": team.name,
                        "logo": team.logo,
                        "created_at": str(team.created_at),
                        "captain": {
                            "fc": team.captain.fc,
                            "discord": d.id if (d := await team.captain.get_discord(ctx)) else team.captain.discord,
                        },
                        "players": [{
                            "raw": player.raw,
                            "created_at": str(player.created_at),
                        } for player in team.players]
                    } for team in battlefy_tourney.teams
                ]
            }
            print(exported_data)
            # Create a file in memory and dump the dictionary into it
            file = StringIO()
            json.dump(exported_data, file)
            file.seek(0)

        # Send the file with an embed
        await ctx.send(
            embed=utils.Embed(
                title=f"📥 **Success:** Exported data for `{tourney.event.name}`",
                description="Froze and exported a compiled report of the tournament data!"),
            file=discord.File(file, filename="export.json"))

    @staticmethod
    def tourney_desc(ctx, tourney):
        """ Format tournament description.

        :param utils.Event tourney: the tournament event object
        """
        format_str = 'MMM DD, YYYY h:mm A UTC'
        text = [
            f"Event Begin Time: `{tourney.event.begin.format(format_str)}`",
            f"Event End Time: `{tourney.event.end.format(format_str)}`",
            f"Captain Role: {tourney.get_role(ctx).mention}",
        ]
        if tourney.battlefy:
            text.append(f"Battlefy Tournament ID: `{tourney.battlefy}`")
        elif tourney.sendou:
            text.append(f"Sendou Tournament ID: `{tourney.sendou}`")
        return "\n".join(text)

    # Captain Command Group:

    @commands.has_role("Staff")
    @commands.group(invoke_without_command=True)
    async def captain(self, ctx, index: int = 0):
        """
        Show the current status of captains.
        Group of commands handling the captain roles.
        """
        await ctx.invoke(self.check, index)  # Run 'captain check' command

    @commands.has_role("Staff")
    @captain.command()
    async def check(self, ctx, index: int = 0, _invalid_captains=None):
        """Show the current status of captains."""
        async with ctx.typing():
            # Get the tournament teams
            tourney = utils.agenda.tourney_at(index)
            if not tourney:
                return await ctx.send("⛔ **No event found**")
            if tourney.battlefy:
                teams = await battlefy.connector.get_teams(tourney.battlefy)
            elif tourney.sendou:
                teams = await self.sendou.get_teams(tourney.sendou)
            else:
                return await ctx.send("⛔ **No platform found**")

            # Create list of invalid captains
            if not _invalid_captains:
                invalid_captains = [
                    f"`{team.captain.discord}` | `{team.name}`" for team in teams
                    if not await team.captain.get_discord(ctx)
                ]
            else:
                invalid_captains = [f"`{team.captain.discord}` | `{team.name}`" for team in _invalid_captains]

            # Send status check embed
            send_file = None
            embed = utils.Embed(
                title=f"🗒️ Captain status check for `{tourney.event.name}`",
                description=f"Invalid Captains / Total Teams: `{len(invalid_captains)}/{len(teams)}`")
            if invalid_captains:
                list_invalid_captains = utils.Embed.list(invalid_captains)
                if len(list_invalid_captains) < 1024:
                    embed.add_field(name="List of invalid captains:", value=list_invalid_captains)
                else:
                    send_file = BytesIO(utils.Embed.file_list(invalid_captains).encode())
            else:
                embed.add_field(
                    name="List of invalid captains:",
                    value="> ✨ **~ No invalid captains! ~**")
            await ctx.send(embed=embed)
            if send_file:
                await ctx.send(content="## File with invalid captains",
                               file=discord.File(fp=send_file, filename="invalid_captains.md"))

    @commands.has_role("Staff")
    @captain.command()
    async def assign(self, ctx, index: int = 0, nick: bool = True):
        """Assign captain role to members."""
        tourney = utils.agenda.tourney_at(index)
        if not tourney:
            return await ctx.send("⛔ **No event found**")
        role = tourney.get_role(ctx)
        valid_captains = []
        invalid_captains = []
        assigned_to = 0

        # Loop over teams and assign valid captains
        async with ctx.typing():
            if tourney.battlefy:
                teams = await battlefy.connector.get_teams(tourney.battlefy)
            elif tourney.sendou:
                teams = await self.sendou.get_teams(tourney.sendou)
            else:
                return await ctx.send("⛔ **No platform found**")
            for team in teams:
                # Attempt to add captain role to members
                try:
                    if (member := await team.captain.get_discord(ctx)) is None:
                        raise discord.DiscordException
                    await member.add_roles(role)
                    valid_captains.append(member)
                    assigned_to += 1
                # Adding role failed, append team to the list of invalid captains
                except discord.DiscordException:
                    invalid_captains.append(team)
                # Adding captain role was successful, optionally edit captain nickname
                else:
                    if nick:
                        await member.edit(nick=team.name[:32])

        # Remove those with the captain role that are not a valid captain
        for member in role.members:
            if member not in valid_captains:
                await member.remove_roles(role)

        # Send Report Embed
        embed = utils.Embed(
            title=f"✅ **Success:** roles assigned for `{tourney.event.name}`",
            description=f"{tourney.get_role(ctx).mention} assigned to `{assigned_to}` members.")
        await ctx.send(embed=embed)
        await ctx.invoke(self.check, index, invalid_captains)  # Run 'captain check' command

    @commands.has_role("Staff")
    @captain.command()
    async def remove(self, ctx, index: int = 0, nick: bool = True):
        """Remove captain role from members."""
        tourney = utils.agenda.tourney_at(index)
        if not tourney:
            return await ctx.send("⛔ **No event found**")
        removed_from = len(tourney.get_role(ctx).members)

        async with ctx.typing():
            # Loop over members with the captain_role
            for member in tourney.get_role(ctx).members:
                await member.remove_roles(tourney.get_role(ctx))
                if nick:
                    await member.edit(nick=None)

        # Display embed
        embed = utils.Embed(
            title=f"❎ **Success:** roles removed for `{tourney.event.name}`",
            description=f"{tourney.get_role(ctx).mention} removed from `{removed_from}` members.")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Tourney(bot))
