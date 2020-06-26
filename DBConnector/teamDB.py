from .models.teamModel import TeamModel
from .errors import MoreThenOneError, CheckInBlockedError
import battlefyConnector
from battlefyConnector import Team, Player
from typing import Optional


class TeamDB:
    def __init__(self, tournamentID: str, discordFieldID: str, FCFieldID: str):
        self.tournamentID = tournamentID
        self.discordFieldID = discordFieldID
        self.FCFieldID = FCFieldID
        self.battlefy = battlefyConnector.BattlefyUtils()

    async def add_teams(self) -> bool:
        teams = await self.battlefy.get_list_of_teams(self.tournamentID, self.discordFieldID, self.FCFieldID)
        if teams is None:
            return False
        for team in teams:
            teamID = team.teamID
            teamName = team.teamName
            discord = team.captainDiscord
            FC = team.captainFC
            captain = team.captain.json_return()
            teamIcon = team.teamIconURL
            model = TeamModel(teamID, teamName=teamName, captainDiscord=discord,
                              captainFC=FC, captain=captain,
                              players=team.player_list(), teamIconURL=teamIcon)
            model.save()
        return True

    async def get_teams_model(self, discordUsername: str = None, teamName: str = None,
                              teamID: str = None, checkIn: bool = None) -> list:
        returnList = []
        if discordUsername:
            for team in TeamModel.scan(TeamModel.captainDiscord == discordUsername):
                returnList.append(team)
            return returnList
        if teamName:
            for team in TeamModel.scan(TeamModel.teamName == teamName):
                returnList.append(team)
            return returnList
        if teamID:
            for team in TeamModel.scan(TeamModel.teamID == teamID):
                returnList.append(team)
            return returnList
        if checkIn is not None:
            for team in TeamModel.scan(TeamModel.checkIN == checkIn):
                returnList.append(team)
            return returnList
        for team in TeamModel.scan():
            returnList.append(team)
        return returnList

    async def update_team_checkin(self, checkinStatus: bool, discordUsername: str = None,
                                  teamName: str = None, teamID: str = None) -> bool:
        teams = None
        if discordUsername:
            teams = await self.get_teams_model(discordUsername=discordUsername)
        if teamName:
            teams = await self.get_teams_model(teamName=teamName)
        if teamID:
            teams = await self.get_teams_model(teamID=teamID)
        if teams is None or len(teams) < 1:
            return False
        if len(teams) > 1:
            raise MoreThenOneError("More then 1 teams returned")
        team = teams[0]
        if team.allowCheckIN is False:
            raise CheckInBlockedError("Checkin disabled for team")
        team.update(
            actions=[
                TeamModel.checkIN.set(checkinStatus)
            ]
        )
        return True

    async def update_allow_checkin(self, checkinAllow: bool, discordUsername: str = None,
                                  teamName: str = None, teamID: str = None) -> bool:
        teams = None
        if discordUsername:
            teams = await self.get_teams_model(discordUsername=discordUsername)
        if teamName:
            teams = await self.get_teams_model(teamName=teamName)
        if teamID:
            teams = await self.get_teams_model(teamID=teamID)
        if teams is None or len(teams) < 1:
            return False
        if len(teams) > 1:
            raise MoreThenOneError("More then 1 teams returned")
        team = teams[0]
        team.update(
            actions=[
                TeamModel.allowCheckIN.set(checkinAllow)
            ]
        )
        return True

    async def get_teams(self, discordUsername: str = None, teamName: str = None,
                        teamID: str = None, checkIN: bool = None) -> Optional[list]:
        if discordUsername:
            teamsModels = await self.get_teams_model(discordUsername=discordUsername)
        elif teamName:
            teamsModels = await self.get_teams_model(teamName=teamName)
        elif teamID:
            teamsModels = await self.get_teams_model(teamID=teamID)
        elif checkIN is not None:
            teamsModels = await self.get_teams_model(checkIn=checkIN)
        else:
            teamsModels = await self.get_teams_model()
        if teamsModels is None or len(teamsModels) < 1:
            return None
        returnList = []
        for teamModel in teamsModels:
            captain = Player()
            captain.load_from_dict(teamModel.captain)
            players = []
            for player in teamModel.players:
                tempPlayer = Player()
                tempPlayer.load_from_dict(player)
                players.append(tempPlayer)
            returnList.append(Team(teamModel.teamName, teamModel.teamID, teamModel.captainDiscord, teamModel.captainFC,
                                   captain, players, teamModel.teamIconURL, teamModel.checkIN, teamModel.allowCheckIN))
        return returnList


