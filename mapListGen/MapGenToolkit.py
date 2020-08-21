"""
This is the actual file discord.py talks to for maps functions
"""
from .errors import *
import discord
from utils import embedder
from typing import Optional
import mapListGen.splatoonSetGen as Splatoon
from .mapStorage import MapSetStorage
from .mapListImageGen import MapSetUpload
import pickle
import os


class MapToolkit:
    def __init__(self, filename: str):
        self.filename = filename
        self.uploader = MapSetUpload()
        if os.path.exists(filename):
            with open(filename, 'rb') as token:
                self.Storage = pickle.load(token)
        else:
            self.Storage = MapSetStorage()
            with open(filename, 'wb') as token:
                pickle.dump(self.Storage, token)

    def __save_pickle(self):
        with open(self.filename, 'wb') as token:
            pickle.dump(self.Storage, token)

    async def setMaps(self, sz: str, tc: str, rm: str, cb: str):
        try:
            self.Storage.setMaps(Splatoon.build_map_pool(sz, tc, rm, cb))
            self.__save_pickle()
            return True
        except NotEnoughMapsException:
            return False

    async def setBrackets(self, bracketString: str):
        try:
            self.Storage.setBracket(Splatoon.build_brackets_from_string(bracketString))
            self.__save_pickle()
            return True
        except ValueError:
            return False

    async def generateBracket(self, seed: int) -> Optional[discord.Embed]:
        if not self.Storage.locked:
            if not self.Storage.Maps or not self.Storage.Bracket:
                return None
            self.Storage.setSet(Splatoon.generate_maps(self.Storage.Maps, self.Storage.Bracket, seed))
            self.__save_pickle()
            return Splatoon.get_map_list_embed(self.Storage.Set)

    async def getBracket(self) -> Optional[discord.Embed]:
        if not self.Storage.Set:
            return None
        return Splatoon.get_map_list_embed(self.Storage.Set)

    async def uploadJSON(self) -> Optional[str]:
        if not self.Storage.Set:
            return None
        response = await self.uploader.uploadJSON(Splatoon.get_map_list_dict(self.Storage.Set))
        return response

    async def toggleLock(self) -> bool:
        self.Storage.toggleLock()
        return self.Storage.locked

    async def getSettings(self) -> discord.Embed:
        embed = await embedder.create_embed("Map Gen Settings", "Current map gen settings")
        if not self.Storage.Bracket:
            embed.add_field(name="Bracket Info:", value="**No Bracket Set**", inline=False)
        else:
            bracketString = "```"
            for item in self.Storage.Bracket:
                bracketString += "\nNumber of Bracket: {}".format(item[0])
                bracketString += "\nBest of: {}".format(item[1])
                bracketString += "\n------"
            bracketString += "\n```"
            embed.add_field(name="Bracket Info:", value=bracketString, inline=False)

        if not self.Storage.Maps:
            embed.add_field(name="Maps", value="**No Maps Set**", inline=False)
        else:
            embed.add_field(name="Splat Zone Maps:",
                            value=await embedder.list_to_code_block(self.Storage.Maps[0]), inline=False)
            embed.add_field(name="Tower Control Maps:",
                            value=await embedder.list_to_code_block(self.Storage.Maps[1]), inline=False)
            embed.add_field(name="Rain Maker Maps:",
                            value=await embedder.list_to_code_block(self.Storage.Maps[2]), inline=False)
            embed.add_field(name="Clam Blitz Maps:",
                            value=await embedder.list_to_code_block(self.Storage.Maps[3]), inline=False)
        if self.Storage.Set:
            embed.add_field(name="Set:", value="**Generated**", inline=False)
        else:
            embed.add_field(name="Set:", value="`None`", inline=False)
        embed.add_field(name="Lock:", value=self.Storage.locked, inline=False)
        return embed
