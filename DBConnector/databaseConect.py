from DBConnector import Team, TeamPlayer, Tournament, TournamentTeam, Player, PlayerObject, TeamObject
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Optional
from datetime import datetime


class DBConnect:
    def __init__(self, databaseString: str):
        self.engine = create_engine(databaseString)
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    async def __getPlayer(self, battlefyID: str = None, playerID: str = None) -> Optional[Player]:
        if battlefyID:
            playerQuery = self.session.query(Player).filter(Player.battlefyID == battlefyID).one()
            if playerQuery:
                return playerQuery
        if playerID:
            playerQuery = self.session.query(Player).filter(Player.playerID == playerID).one()
            if playerQuery:
                return playerQuery
        return None

    async def __updatePlayer(self, player: PlayerObject) -> PlayerObject:
        playerQuery = self.session.query(Player).filter(Player.battlefyID == player.battlefyPlayerID)
        if not playerQuery.all():
            # If item isn't in database, we add it
            newPlayer = Player(battlefyID=player.battlefyPlayerID, inGameName=player.inGameName,
                               battlefyUserslug=player.battlefyUserslug, previousIGN=player.previousIGN,
                               discordID=player.discordID)
            self.session.add(newPlayer)
            self.session.flush()
            self.session.commit()
            player.setID(newPlayer.playerID)
        else:  # if Item is already in DB
            playerReturn = playerQuery.one()
            player.setID(playerReturn.playerID)
            # We can assume the playerID and battlefyID are unique and don't need checked.
            # Merge the list of previous names given in the DB with the ones given, and remove duplicates
            player.setPreviousIGN(list(set(player.previousIGN + playerReturn.previousIGN)))
            if player.inGameName != playerReturn.inGameName:
                formerNames = playerReturn.previousIGN
                formerNames.append(playerReturn.inGameName)
                formerNames = list(set(formerNames))  # removes any duplicate from the list
                player.setPreviousIGN(formerNames)
            if player.discordID is None:
                player.setDiscordID(playerReturn.discordID)
            if player.previousIGN is None:
                player.setPreviousIGN(playerReturn.previousIGN)
            playerQuery.update({Player.inGameName: player.inGameName,
                                Player.battlefyUserslug: player.battlefyUserslug,
                                Player.previousIGN: player.previousIGN,
                                Player.discordID: player.discordID})
            self.session.commit()
        return player

    async def __updateTeams(self, team: TeamObject) -> TeamObject:
        teamQuery = self.session.query(Team).filter(Team.battlefyID == team.battlefyID)
        if not teamQuery.all():
            newTeam = Team(battlefyID=team.battlefyID, teamName=team.teamName, iconURL=team.teamIcon)
            self.session.add(newTeam)
            self.session.flush()
            self.session.commit()
            team.setID(newTeam.teamID)
        else:
            team.setID(teamQuery.all()[0].teamID)
            teamQuery.update({Team.teamName: team.teamName,
                              Team.iconURL: team.teamIcon})
            self.session.commit()
        return team

    async def __addTeamPlayers(self, teamID: int, playerID: int, joinDate: datetime, admin: bool) -> bool:
        teamPlayerQuery = self.session.query(TeamPlayer).filter(TeamPlayer.tournamentTeamID == teamID). \
            filter(TeamPlayer.playerID == playerID)
        if not teamPlayerQuery.all():
            newTeamPlayer = TeamPlayer(tournamentTeamID=teamID, playerID=playerID, joinDate=joinDate, admin=admin)
            self.session.add(newTeamPlayer)
            self.session.flush()
            self.session.commit()
            return True
        return False

    async def addTournament(self, battlefyID: str, date: datetime, guildID: str, roleID: str) -> bool:
        tournamentQuery = self.session.query(Tournament).filter(Tournament.battlefyID == battlefyID)
        if not tournamentQuery.all():  # if tournaments doesn't exist in DB
            newTournament = Tournament(battlefyID=battlefyID, date=date, guildID=guildID, roleID=roleID)
            self.session.add(newTournament)
            self.session.flush()
            self.session.commit()
            return True
        else:
            return False

    async def updateTournamentTeam(self, team: TeamObject, tournamentBattlefyID: str):
        team = await self.__updateTeams(team)  # Add/Update the team entry itself
        tournament = self.session.query(Tournament).filter(Tournament.battlefyID == tournamentBattlefyID).all()[0]
        tournamentTeamQuery = self.session.query(TournamentTeam). \
            filter(TournamentTeam.tournamentID == tournament.tournamentID). \
            filter(TournamentTeam.teamID == team.ID)
        if not tournamentTeamQuery.all():  # if team isn't in DB for tournament add it
            newTournamentTeam = TournamentTeam(tournamentID=tournament.tournamentID, teamID=team.ID,
                                               joinDate=team.joinDate, captainDiscord=team.captainDiscord,
                                               captainFC=team.captainFC, bracket=team.bracket,
                                               allowCheckin=team.allowCheckin, checkin=team.checkin,
                                               manualPlayers=team.manualPlayers)
            self.session.add(newTournamentTeam)
            self.session.flush()
            self.session.commit()
            team.setID(newTournamentTeam.ID)
            tournamentReturn = newTournamentTeam
        else:  # Else just update the fields if there is already an instance
            tournamentTeamQuery.update({TournamentTeam.captainDiscord: team.captainDiscord,
                                        TournamentTeam.captainFC: team.captainFC,
                                        TournamentTeam.manualPlayers: team.manualPlayers})
            self.session.commit()
            tournamentReturn = tournamentTeamQuery.one()
            team.setID(tournamentReturn.ID)
        newPlayerList = []  # This list stores the players are they added/updated
        for player in team.players:  # for all the players we have
            # Add/update there DB entry and add to the list we made
            newPlayerList.append(await self.__updatePlayer(player))
        for player in newPlayerList:  # This loop creates the link between the team and player for the tournament
            await self.__addTeamPlayers(tournamentReturn.ID, player.ID, player.createdAt, player.admin)
        # Here we getting all the players we have linked to the team for this tournament
        teamPlayers = self.session.query(TeamPlayer).filter(TeamPlayer.tournamentTeamID == tournamentReturn.ID)
        # Go through the list of linked players to see if we have any that aren't meant to be there now (i.e. deleted)
        for player in teamPlayers:
            playerInstance = self.session.query(Player).filter(Player.playerID == player.playerID).all()
            if playerInstance:
                if not team.gotPlayer(playerInstance[0].battlefyID):
                    self.session.delete(player)
                    self.session.commit()

    async def __get_TournamentTeam(self, tournamentID: str, teamName: str = None,
                                   captainDiscordUsername: str = None, teamID: str = None):
        if teamName:
            return self.session.query(TournamentTeam).join(Team).join(Tournament). \
                filter(Team.teamName == teamName).filter(Tournament.battlefyID == tournamentID)
        elif captainDiscordUsername:
            return self.session.query(TournamentTeam).join(Tournament). \
                filter(TournamentTeam.captainDiscord == captainDiscordUsername). \
                filter(Tournament.battlefyID == tournamentID)
        elif teamID:
            return self.session.query(TournamentTeam).join(Team).join(Tournament). \
                filter(Team.battlefyID == teamID). \
                filter(Tournament.battlefyID == tournamentID)
        else:
            return None

    async def set_bracket(self, bracket: int, tournamentID: str, teamName: str = None,
                          captainDiscordUsername: str = None, teamID: str = None) -> Optional[bool]:
        # This queries for the TournamentTeam with the teamName and tournamentID matching
        if teamName:
            queryReturn = await self.__get_TournamentTeam(tournamentID, teamName=teamName)
        elif captainDiscordUsername:
            queryReturn = await self.__get_TournamentTeam(tournamentID, captainDiscordUsername=captainDiscordUsername)
        elif teamID:
            queryReturn = await self.__get_TournamentTeam(tournamentID, teamID=teamID)
        else:
            return None
        if queryReturn.all() is False:  # No team found
            return None
        if len(queryReturn.all()) > 1:  # More then one team found
            return False
        queryReturn.update({TournamentTeam.bracket: bracket})
        return True

    async def set_allow_checkin(self, allowCheckin: bool, tournamentID: str, teamName: str = None,
                                captainDiscordUsername: str = None, teamID: str = None) -> Optional[bool]:
        # This queries for the TournamentTeam with the teamName and tournamentID matching
        if teamName:
            queryReturn = await self.__get_TournamentTeam(tournamentID, teamName=teamName)
        elif captainDiscordUsername:
            queryReturn = await self.__get_TournamentTeam(tournamentID, captainDiscordUsername=captainDiscordUsername)
        elif teamID:
            queryReturn = await self.__get_TournamentTeam(tournamentID, teamID=teamID)
        else:
            return None
        if queryReturn.all() is False:  # No team found
            return None
        if len(queryReturn.all()) > 1:  # More then one team found
            return False
        queryReturn.update({TournamentTeam.allowCheckin: allowCheckin})
        return True

    async def set_checkin(self, checkin: bool, tournamentID: str, teamName: str = None,
                          captainDiscordUsername: str = None, teamID: str = None) -> Optional[bool]:
        # This queries for the TournamentTeam with the teamName and tournamentID matching
        if teamName:
            queryReturn = await self.__get_TournamentTeam(tournamentID, teamName=teamName)
        elif captainDiscordUsername:
            queryReturn = await self.__get_TournamentTeam(tournamentID, captainDiscordUsername=captainDiscordUsername)
        elif teamID:
            queryReturn = await self.__get_TournamentTeam(tournamentID, teamID=teamID)
        else:
            return None
        if len(queryReturn.all()) > 1:  # More then one team found
            return False
        queryReturn.update({TournamentTeam.checkin: checkin})
        return True

    async def get_teams(self, tournamentID: str, teamName: str = None,
                        captainDiscordUsername: str = None, teamID: str = None) -> Optional[list]:
        if teamName:
            queryReturn = await self.__get_TournamentTeam(tournamentID, teamName=teamName)
        elif captainDiscordUsername:
            queryReturn = await self.__get_TournamentTeam(tournamentID, captainDiscordUsername=captainDiscordUsername)
        elif teamID:
            queryReturn = await self.__get_TournamentTeam(tournamentID, teamID=teamID)
        else:
            return None
        returnTeamList = []
        for team in queryReturn.all():
            teamPlayers = []
            for entry in team.players:
                teamPlayers.append(PlayerObject(ID=entry.Player.playerID, battlefyPlayerID=entry.Player.battlefyID,
                                                battlefyUserslug=entry.Player.battlefyUserslug,
                                                inGameName=entry.Player.inGameName,
                                                previousIGN=entry.Player.previousIGN,
                                                discordID=entry.Player.discordID, createdAt=entry.joinDate.isoformat(),
                                                admin=entry.admin))
            returnTeamList.append(TeamObject(ID=team.ID, battlefyID=team.team.battlefyID, teamName=team.team.teamName,
                                             teamIcon=team.team.iconURL, joinDate=team.joinDate,
                                             captainDiscord=team.captainDiscord, captainFC=team.captainFC,
                                             players=teamPlayers, manualPlayers=team.manualPlayers,
                                             allowCheckin=team.allowCheckin, checkin=team.checkin,
                                             bracket=team.bracket))
        return returnTeamList

    async def get_all_teams(self, tournamentID: str):
        query = self.session.query(TournamentTeam).join(Tournament)\
            .filter(Tournament.battlefyID == tournamentID)
        returnTeamList = []
        for team in query.all():
            teamPlayers = []
            for entry in team.players:
                teamPlayers.append(PlayerObject(ID=entry.Player.playerID, battlefyPlayerID=entry.Player.battlefyID,
                                                battlefyUserslug=entry.Player.battlefyUserslug,
                                                inGameName=entry.Player.inGameName,
                                                previousIGN=entry.Player.previousIGN,
                                                discordID=entry.Player.discordID, createdAt=entry.joinDate.isoformat(),
                                                admin=entry.admin))
            returnTeamList.append(TeamObject(ID=team.ID, battlefyID=team.team.battlefyID, teamName=team.team.teamName,
                                             teamIcon=team.team.iconURL, joinDate=team.joinDate,
                                             captainDiscord=team.captainDiscord, captainFC=team.captainFC,
                                             players=teamPlayers, manualPlayers=team.manualPlayers,
                                             allowCheckin=team.allowCheckin, checkin=team.checkin,
                                             bracket=team.bracket))
        return returnTeamList
