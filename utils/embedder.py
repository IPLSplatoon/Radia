import discord
import datetime


async def create_embed(title=None, description=None, url=None) -> discord.Embed:
    """
    Creates a discord embed template
    :param title: str
        Title for embed
    :param description: str
        Description for embed
    :param url: str
        URL for embed
    :return: discord.embed
        discord.py embed object
    """
    embed = discord.Embed(title=title, description=description, url=url, color=0xe0fe3a)
    embed.set_author(name="Radia", url="https://battlefy.com/low-ink",
                     icon_url="https://cdn.vlee.me.uk/LowInk/LowInkIcon.png")
    embed.set_footer(text="The Low Ink Bot", icon_url="https://cdn.vlee.me.uk/LowInk/LowInk.png")
    embed.timestamp = datetime.datetime.utcnow()
    return embed


async def list_to_code_block(message: list) -> str:
    """
    Turns a list into a code block with each item on a new line in a list with a -
    :param message: list
        List to turn into code block
    :return: str
        Str code block
    """
    codeBlock = "```\n"
    for items in message:
        codeBlock = codeBlock + "- {}\n".format(items)
    return codeBlock + "```"
