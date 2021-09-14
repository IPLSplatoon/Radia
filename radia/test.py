import asyncio
from smashgg import Connector

async def main():
    smashgg = Connector("151e771f9b40b0acbb0d79b340690d67")
    tournament = await smashgg.get_tournament("superjump-1")
    for e in tournament.events:
        if e.name == "Splatoon 2":
            teams = await e.get_teams()
            for t in teams:
                print(t)
    print(tournament.name)
    print(tournament.id)



loop = asyncio.get_event_loop()
loop.run_until_complete(main())
