import motor.motor_asyncio

import discord
from discord.ext import commands

from .errors import CaptainNotFound, RoleNotFound


class MongoTeam:
    """Represents a team stored in MongoDB"""
    def __init__(self, mongo_object: dict, collection: motor.motor_asyncio.AsyncIOMotorCollection):
        """
        Init
        :param mongo_object: MongoDB document
        :param collection: MongoDB Collection connection
        """
        self._collection = collection

        self.team_id = mongo_object.get("_id")
        self.battlefy_tournament_id = mongo_object.get("battlefyTournamentId")
        self.name = mongo_object.get("name")
        self.logo_icon = mongo_object.get("logoUrl", None)
        self.captain_discord = mongo_object.get("captainDiscord")
        self.additional_discord = mongo_object.get("additionalDiscord", [])
        self.bracket = mongo_object.get("bracket", 0)
        self.checkin = mongo_object.get("checkin", False)

    async def set_check_in(self, status: bool = True) -> bool:
        """
        Check in the team
        :param status: Check in status
        :return: success status
        """
        update = await self._collection.update_one(
            {"name": self.name, "battlefyTournamentId": self.battlefy_tournament_id},
            {"$set": {"checkin": status}}, upsert=True)
        if update:
            self.checkin = status
            return True
        else:
            return False

    async def set_bracket(self, bracket: int) -> bool:
        """
        Set team's bracket
        :param bracket: Bracket to set
        :return: success status
        """
        update = await self._collection.update_one(
            {"name": self.name, "battlefyTournamentId": self.battlefy_tournament_id},
            {"$set": {"bracket": bracket}}, upsert=True)
        if update:
            self.bracket = bracket
            return True
        else:
            return False

    async def set_captain_discord(self, captain_discord: str) -> bool:
        """
        Set team's bracket
        :param captain_discord: captain username#tag
        :return: success status
        """
        update = await self._collection.update_one(
            {"name": self.name, "battlefyTournamentId": self.battlefy_tournament_id},
            {"$set": {"captainDiscord": captain_discord}}, upsert=True)
        if update:
            self.captain_discord = captain_discord
            return True
        else:
            return False

    async def add_additional_discord(self, discord_field: str) -> bool:
        """
        Add additional Discord to team
        :param discord_field: Discord ID
        :return: success status
        """
        update = await self._collection.update_one(
            {"name": self.name, "battlefyTournamentId": self.battlefy_tournament_id},
            {"$set": {"additional_discord": {"$each": [discord_field]}}}, upsert=True)
        if update:
            self.additional_discord.append(discord)
            return True
        else:
            return False

    async def set_assign_bracket(self, ctx: commands.Context, bracket_info: dict) -> bool:
        """
        Assign Role and set bracket
        :param ctx: Discord Context
        :param bracket_info: format like so {"name": "ALPHA", "id": 1}
        :return: success status
        """
        if not self.captain_discord:
            raise CaptainNotFound
        try:
            # If we can't find the person stated on the discord field in the server
            if not (captain := await commands.MemberConverter().convert(ctx, self.captain_discord)):
                raise CaptainNotFound
        except commands.BadArgument:  # catch all for above
            raise CaptainNotFound
        try:
            if not (role := discord.utils.get(ctx.guild.roles, name=f"{bracket_info['name']}")):
                raise RoleNotFound
            await captain.add_roles(role)
            return await self.set_bracket(bracket_info['id'])
        except discord.Forbidden:
            pass
