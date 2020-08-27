"""
Contains HelpCommand class.

Stole directly from "https://github.com/offthedial/bot/blob/master/offthedialbot/help.py"
Thank me :)
"""

import discord
from discord.ext import commands

from .embed import create as embedder


class HelpCommand(commands.DefaultHelpCommand):
    """Set up help command for the bot."""

    async def send_bot_help(self, mapping):
        """Send bot command page."""
        embed = self.create_embed(
            title="`!help`",
            fields=[{
                "name": cog.qualified_name if cog else '\u200B',
                "value": "\n".join([
                    self.short(command)
                    for command in await self.filter_commands(cog_commands)
                ])} for cog, cog_commands in mapping.items() if await self.filter_commands(cog_commands)][::-1]
        )
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        """Send cog command page."""
        embed = self.create_embed(
            title=cog.qualified_name.capitalize(),
            description=cog.description,
            **({"fields": [{
                "name": f"{cog.qualified_name.capitalize()} Commands:",
                "value": "\n".join([
                    self.short(command)
                    for command in cog.get_commands()])
            }]} if cog.get_commands() else {}))

        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        """Send command group page."""
        embed = self.create_embed(
            title=self.short(group, False),
            description=group.help,
            fields=[{
                "name": f"Subcommands:",
                "value": "\n".join([
                    self.short(command)
                    for command in await self.filter_commands(group.all_commands.values())
                ])
            }]
        )
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        """Send command page."""
        embed = self.create_embed(
            title=self.short(command, False),
            description=command.help,
        )
        await self.get_destination().send(embed=embed)

    async def command_not_found(self, string):
        """Returns message when command is not found."""
        return f"Command {self.short(string, False)} does not exist."

    async def subcommand_not_found(self, command, string):
        """Returns message when subcommand is not found."""
        message = super().subcommand_not_found(command, string).split()
        message[1] = f'`{self.clean_prefix}{message[1][1:-1]}`'
        if not message[-1].endswith("."):
            message[-1] = f'`{message[-1]}`.'
        return " ".join(message)

    async def send_error_message(self, error):
        """Send error message, override to support sending embeds."""
        await self.get_destination().send(embed=embedder(title="Command/Subcommand not found.", description=error))

    def create_embed(self, fields: list = (), **kwargs):
        """Create help embed."""
        embed = embedder(**kwargs)
        for field in fields:
            embed.add_field(**field, inline=False)
        embed.set_footer(
            text=f"Type {self.clean_prefix}help command for more info on a command. You can also type {self.clean_prefix}help category for more info on a category.")
        return embed

    def short(self, command, doc=True):
        """List the command as a one-liner."""
        return f'`{self.clean_prefix}{command}` {(command.short_doc if doc else "")}'
