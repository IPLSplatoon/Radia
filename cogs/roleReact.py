"""
This cog configures, loads and runs Reaction based role requests
"""
import utils
from discord.ext import commands, tasks
import discord
import gSheetConnector
import datetime
import os
from dotenv import load_dotenv
import emoji
import re

load_dotenv("files/.env")
GOOGLE_SHEET_NAME = os.environ.get("google_sheet_name")


def emoji_check(emojiChar: str):
    """
    Check if the emoji provided is custom, or unicode
    :param emojiChar: str
    :return: int, str
        int: 0 = Invalid, 1 = Unicode, 2 = Custom
        str: ID, Unicode Codestring, None
    """
    # Check if it's an Unicode emoji
    if emojiChar in emoji.UNICODE_EMOJI:
        try:  # Try catch cause some emoji use a string length of 2 (E.g. flags) and they aren't supported
            returnStr = 'U+{}'.format(ord(emojiChar))
            return 1, returnStr  # Last section gets the unicode code
        except TypeError:  # If we run into a type error we return is as if it isn't an emoji
            return 0, None
    # This is a regular expression to check the format for a Discord custom Emoji
    customEmojiExpression = re.compile("<:([A-Z]*[a-z]*[0-9]*[_]*){2,}:([0-9]+)>")
    # Check if the emoji is a custom emoji
    if customEmojiExpression.match(emojiChar):
        emojiChar = emojiChar[2:][:-1]  # Remove first 2 and last char from string
        emojiID = emojiChar.split(":")  # Split string with the : in the middle
        return 2, emojiID[1]  # Return
    return 0, None  # Return 0 and None is provided string isn't an emoji


class RoleReact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sheets = gSheetConnector.SheetConnector("files/googleAuth.json", GOOGLE_SHEET_NAME)
        self.roleDB = utils.RoleReactList("files/roleDB.p")

    @commands.has_role("Staff")
    @commands.guild_only()
    @commands.command(name='addReaction', help="Add a Reaction and Role to give out.\n"
                                               "<messageID>: The message ID of the reaction you want to add to.\n"
                                               "<emote>: The emote you want to use.\n"
                                               "<roleID>: ID of the role you want to assign")
    async def add_react_role(self, ctx, messageID, emote, roleID):
        with ctx.typing():
            roleToAssign = discord.utils.get(ctx.message.guild.roles, id=int(roleID))
            # Check if role exists
            if roleToAssign is None:
                embed = await utils.create_embed("Reaction Role Add Error",
                                                 "Unable to find role with ID: {}".format(roleID))
                await ctx.send(embed=embed)
                return
            # Checks if message exists
            try:
                message = await ctx.message.channel.fetch_message(int(messageID))
            except discord.NotFound:
                embed = await utils.create_embed("Reaction Role Add Error",
                                                 "Message does not exist with ID: {}".format(messageID))
                await ctx.send(embed=embed)
                return
            except discord.HTTPException:
                embed = await utils.create_embed("Reaction Role Add Error",
                                                 "Unable to find message with ID: {}".format(messageID))
                await ctx.send(embed=embed)
                return
            # Get and check emote
            try:
                emoteType, emoteID = emoji_check(emote)
                if emoteType == 1:  # if Emote is an unicode emoji
                    if await self.roleDB.add_message_reaction(messageID, emoteID, roleID):
                        await message.add_reaction(chr(int((emoteID[2:]))))
                    else:
                        embed = await utils.create_embed("Reaction Role Add Error",
                                                         "Unable add to database: {}".format(messageID))
                        await ctx.send(embed=embed)
                        return
                elif emoteType == 2:  # if Emote is a custom emoji
                    if await self.roleDB.add_message_reaction(messageID, emoteID, roleID):
                        await message.add_reaction(emote[1:][:-1])
                    else:
                        embed = await utils.create_embed("Reaction Role Add Error",
                                                         "Unable add to database: {}".format(messageID))
                        await ctx.send(embed=embed)
                        return
                else:  # if invalid emote
                    embed = await utils.create_embed("Reaction Role Add Error",
                                                     "Invalid emote: {}".format(emote))
                    await ctx.send(embed=embed)
                    return
                # if we have added the role without error
                embed = await utils.create_embed("Reaction Role Added",
                                                 "You can delete your command and this message now")
                await ctx.send(embed=embed)
                return
            except discord.DiscordException as e:  # Catch errors
                utils.errorCollector.collect_error(e, "Add react role")

    @commands.has_role("Staff")
    @commands.guild_only()
    @commands.command(name='removeReaction', help="Remove a Reaction and Role to give out.\n"
                                                  "<messageID>: The message ID of the reaction you want to add to.\n"
                                                  "<emote>: The emote you want to use.")
    async def remove_react_role(self, ctx, messageID, emote):
        with ctx.typing():
            emoteType, emoteID = emoji_check(emote)
            if emoteType == 1 or 2:
                if await self.roleDB.remove_message_reaction(messageID, emoteID):
                    try:
                        message = await ctx.message.channel.fetch_message(int(messageID))
                        # check emote type and remove the reactions for it
                        if emoteType == 1:
                            await message.clear_reaction(emote)
                        if emoteType == 2:
                            await message.clear_reaction(emote[1:][:-1])
                    except discord.DiscordException as e:
                        utils.errorCollector.collect_error(e, "Role reaction removal")
                    embed = await utils.create_embed("Reaction Role Removed",
                                                     "You can delete your command and this message and the reactions now")
                    await ctx.send(embed=embed)
                    return
                else:
                    embed = await utils.create_embed("Reaction Role Remove Error",
                                                     "Invalid emote: {}".format(emote))
                    await ctx.send(embed=embed)
                    return
            else:
                embed = await utils.create_embed("Reaction Role Remove Error",
                                                 "Invalid emote: {}".format(emote))
                await ctx.send(embed=embed)
                return


    @commands.guild_only()
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # checks type to get emoji name/id for storage
        if payload.emoji.is_custom_emoji():
            emojiID = payload.emoji.id
        else:
            emojiID = emoji_check(payload.emoji.name)[1]
        # Get the role it might corresponds to from DB
        role = await self.roleDB.get_reaction_role(str(payload.message_id), str(emojiID))
        guild = self.bot.get_guild(payload.guild_id)  # Get guild object
        user = discord.utils.get(guild.members, id=payload.user_id)  # get user object
        if role is not None:  # If the role isn't None
            role = discord.utils.get(guild.roles, id=int(role))  # get role object
            botRole = discord.utils.get(guild.roles, name="Radia")  # Get bot's role
            if botRole > role:  # We check the role we assign is bellow the bot's role for sanity reasons
                if role not in user.roles:  # if the user doesn't have the role, give them the role
                    await user.add_roles(role, reason="React Role assignment")
        else:  # If reaction is added to a message that's taking role reactions
            if await self.roleDB.message_in_db(str(payload.message_id)):
                channel = discord.utils.get(guild.text_channels, id=payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                # We remove the invalid reactions
                if payload.emoji.is_custom_emoji():
                    await message.remove_reaction(":{}:{}".format(payload.emoji.name, payload.emoji.id), user)
                else:
                    await message.remove_reaction(payload.emoji.name, user)

    @commands.guild_only()
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # checks type to get emoji name/id for storage
        if payload.emoji.is_custom_emoji():
            emojiID = payload.emoji.id
        else:
            emojiID = emoji_check(payload.emoji.name)[1]
        # Get the role it might corresponds to from DB
        role = await self.roleDB.get_reaction_role(str(payload.message_id), str(emojiID))
        if role is not None:  # If the role isn't None
            guild = self.bot.get_guild(payload.guild_id)  # Get guild object
            role = discord.utils.get(guild.roles, id=int(role))  # get role object
            botRole = discord.utils.get(guild.roles, name="Radia")  # Get bot's role
            user = discord.utils.get(guild.members, id=payload.user_id)  # get user object
            if botRole > role:  # We check the role we assign is bellow the bot's role for sanity reasons
                if role in user.roles:  # if the user doesn't have the role, give them the role
                    await user.remove_roles(role, reason="React Role Removal")


def setup(bot):
    bot.add_cog(RoleReact(bot))
