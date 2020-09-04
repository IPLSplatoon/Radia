"""Utilites to help with roles."""

import discord


def get(ctx, *names):
    """Get a list of all the roles with the given role names."""
    return [
        discord.utils.get(ctx.guild.roles, name=name)
        for name in names
        if discord.utils.get(ctx.guild.roles, name=name)
    ]
