from .connect import Connect
from .team import Team
from typing import List
from aiographql.client import GraphQLRequest


class Event:
    def __init__(self, event: dict, gql_connector: Connect):
        self._raw = event
        self.id: int = self._raw.get("id", None)
        self.name = self._raw.get("name", None)
        self.session = gql_connector

    def _get_entrants_request(self, page: int, per_page: int):
        return GraphQLRequest(
            """
            query EventEntrants($eventId: ID!, $page: Int!, $perPage: Int!) {
              event(id: $eventId) {
                entrants(query: {
                  page: $page
                  perPage: $perPage
                }) {
                  pageInfo {
                    total
                    totalPages
                  }
                  nodes {
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
            """,
            variables={
                "eventId": self.id,
                "page": page,
                "perPage": per_page
            }
        )

    async def get_teams(self) -> List[Team]:
        per_page = 30
        teams = []
        initial_request = await self.session.client.query(self._get_entrants_request(1, per_page))
        initial_data = initial_request.data
        if initial_data["event"]:
            for t in initial_data["event"]["entrants"]["nodes"]:
                teams.append(Team(t))
            pages = initial_data["event"]["entrants"]["pageInfo"]["totalPages"]
            if pages > 1:
                for x in range(2, pages+1):
                    data = (await self.session.client.query(self._get_entrants_request(x, per_page))).data
                    if data["event"]:
                        for t in data["event"]["entrants"]["nodes"]:
                            teams.append(Team(t))
        return teams



