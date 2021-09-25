from aiographql.client import GraphQLRequest
from typing import List
from .team import Team
from .connect import Connect
from .wave import Wave


class PhaseGroup:
    def __init__(self, phase_group_data: dict, gql_connector: Connect):
        self._raw = phase_group_data
        self.session = gql_connector
        self._phase = self._raw.get("phase", {})
        self.phase_name = self._phase.get("name", "")
        self.id: int = self._raw.get("id", None)
        self.display_identifier = self._raw.get("displayIdentifier", None)
        if self._raw["wave"]:
            self.wave = Wave(self._raw["wave"])
        else:
            self.wave = None

    def _get_entrants_request(self, page: int, per_page: int):
        return GraphQLRequest(
            """
            query PhaseGroupEntrants($phaseGroupID: ID!, $page: Int!, $perPage: Int!) {
                phaseGroup(id: $phaseGroupID){
                    seeds(query: {
                        page: $page
                        perPage: $perPage
                    }){
                    pageInfo{
                        total
                        totalPages
                    }
                    nodes{
                        entrant{
                            name
                            team{
                                members{
                                isCaptain
                                participant{
                                    gamerTag
                                    requiredConnections{
                                        externalId
                                        type
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
            """,
            variables={
                "phaseGroupID": self.id,
                "page": page,
                "perPage": per_page
            }
        )

    async def get_teams(self) -> List[Team]:
        per_page = 30
        teams = []
        initial_request = await self.session.client.query(self._get_entrants_request(1, per_page))
        initial_data = initial_request.data
        if initial_data["phaseGroup"]:
            for t in initial_data["phaseGroup"]["seeds"]["nodes"]:
                if t["entrant"]:
                    teams.append(Team(t["entrant"]))
            pages = initial_data["phaseGroup"]["seeds"]["pageInfo"]["totalPages"]
            if pages > 1:
                for x in range(2, pages + 1):
                    data = (await self.session.client.query(self._get_entrants_request(x, per_page))).data
                    if data["phaseGroup"]:
                        for t in data["phaseGroup"]["seeds"]["nodes"]:
                            if t["entrant"]:
                                teams.append(Team(t["entrant"]))
        return teams

