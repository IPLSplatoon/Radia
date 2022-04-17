from aiographql.client import GraphQLClient


class Connect:
    def __init__(self, smashgg_api_key: str):
        self.api_key = smashgg_api_key
        self.client: GraphQLClient = GraphQLClient(
            endpoint="https://api.smash.gg/gql/alpha",
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
