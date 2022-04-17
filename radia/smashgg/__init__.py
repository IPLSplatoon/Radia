from typing import Optional
from aiographql.client import GraphQLRequest
from .objects import Tournament, Connect
import logging
import os


class Connector:
    def __init__(self, api_key: str):
        self._api_key = api_key
        self.session = Connect(self._api_key)
        logging.debug("Loaded smashgg.connector")

    async def get_tournament(self, slug: str) -> Optional[Tournament]:
        request = GraphQLRequest("""
            query TournamentQuery($slug: String) {
                tournament(slug: $slug){
                    id
                    name
                    events {
                        id
                        name
                        phaseGroups{
                            displayIdentifier
                            id
                            phase{
                                name
                            }
                            wave{
                                id
                                identifier
                            }
                        }
                    }
                }
            }
        """, variables={
            "slug": slug
        })
        response = await self.session.client.query(request)
        data = response.data
        if data["tournament"]:
            return Tournament(data["tournament"], self.session)


if not (api_key := os.getenv("SMASHGGAPIKEY")):
    logging.error(".env - 'SMASHGGAPIKEY' key not found. Cannot start bot.")
    raise EnvironmentError

connector = Connector(api_key)
