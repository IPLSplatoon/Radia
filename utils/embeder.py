import discord
import datetime


async def create_embed(title=None, description=None, url=None) -> discord.Embed:

    embed = discord.Embed(title=title, description=description, url=url, color=0x15b22f)
    embed.set_author(name="Radia", url="https://battlefy.com/low-ink",
                     icon_url="https://cdn.vlee.me.uk/LowInk/LowInkIcon.png")
    embed.set_footer(text="The Low Ink Bot", icon_url="https://cdn.vlee.me.uk/LowInk/LowInk.png")
    embed.timestamp = datetime.datetime.utcnow()
    return embed


async def list_to_code_block(message: list) -> str:
    """
    Turns a list into a code block with each item on a new line
    :param message: list
        List to turn into code block
    :return: str
        Str code block
    """
    codeBlock = "```\n"
    for items in message:
        codeBlock = codeBlock + "- {}\n".format(items)
    return codeBlock + "```"
