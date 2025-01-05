import asyncio
from time import time

from socketio import AsyncClient

from game.entity_list import EntityList


async def player_dot(sio: AsyncClient) -> None:
    player_dot_data = list()
    for player_entity in EntityList.player_entities:
        if not player_entity: continue
        if not player_entity.health: continue
        if (pos := player_entity.pos) is None: continue
        if (direction := player_entity.angle) is None: continue

        if (team_num := player_entity.team_num) is None: team_num = 0
        if (steam_id := player_entity.steam_id) is None: steam_id = 0
        if (name := player_entity.name) is None: name = None
        if (team_color := player_entity.team_color) is None: team_color = -1

        player_dot_data.append(dict(
            pos=pos.__dict__,
            direction=direction.__dict__,
            team_num=team_num,
            steam_id=steam_id,
            name=name,
            team_color=team_color
        ))

    if sio.connected:
        await sio.call('player_dot', dict(
            t=time(),
            players=player_dot_data
        ), timeout=1)
