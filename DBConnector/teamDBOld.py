from .models.teamModel import TeamModel
from .errors import MoreThenOneError, CheckInBlockedError
from typing import Optional


class TeamDB:
    def __init__(self, tournamentID: str, discordFieldID: str, FCFieldID: str):
        """
        Constructor
        :param tournamentID:
            tournament ID
        :param discordFieldID:
            fieldID of the discord username
        :param FCFieldID:
            fieldID of Friend code
        """
        self.tournamentID = tournamentID
        self.discordFieldID = discordFieldID
        self.FCFieldID = FCFieldID
        self.battlefy = battlefyConnector.BattlefyUtils()

    async def add_teams(self) -> bool:
        """
        Adds teams into DB from battlefy
        :return: bool
            if tasks was successful or not.
        """
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
        """
        Gets a list of teams matching query
        :param discordUsername: str
            discord name query
        :param teamName: str
            team name query
        :param teamID: str
            teamID query
        :param checkIn: bool
            checkin query
        :return: list
            List of teams that match query
        """
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
        """
        Update team's checkin status
        :param checkinStatus: bool
            checkin status to be set as:
        :param discordUsername: str
            discord name query
        :param teamName: str
            team name query
        :param teamID: str
            teamID query
        :return: bool
            if successful or not
        """
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
        """
        Update the allowCheckIn status of a team
        :param checkinAllow: bool
            checkinAllow status to be set as:
        :param discordUsername: str
            discord name query
        :param teamName: str
            team name query
        :param teamID: str
            teamID query
        :return: bool
            if successful or not
        """
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
        """
        Get a list of Team objects from query
        :param discordUsername: str
            discord name query
        :param teamName: str
            team name query
        :param teamID: str
            teamID query
        :param checkIN: bool
            checkin query
        :return: list
            List of Team objects
        """
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


