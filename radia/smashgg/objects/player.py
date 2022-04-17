from discord.ext import commands


class Player:
    def __init__(self, smashgg: dict):
        self._raw: dict = smashgg
        self.member_converter = commands.MemberConverter()
        self.captain: bool = self._raw.get("isCaptain", False)
        self.participant: dict = self._raw.get('participant', {})
        self.name: str = self.participant.get("gamerTag", "")
        self.discord: str = ""
        required_connections = self.participant.get("requiredConnections", [])
        if required_connections:
            for x in required_connections:
                if x.get("type") == "DISCORD":
                    self.discord: str = x.get("externalId", "")

    async def get_discord(self, ctx):
        """ Return the discord member object using the discord field provided.

        :return Optional[discord.Member]:
            Returns None if the member isn't found in the server.
        """
        if not self.discord:
            return None
        try:
            return await self.member_converter.convert(ctx, self.discord)
        except commands.BadArgument:
            return None
