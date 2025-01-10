import asyncio
from time import time

from memprocfs import FLAG_NOCACHE
from memprocfs.vmmpyc import VmmScatterMemory
from socketio import AsyncClient

from game.entity_list import EntityList
from memory.memory import VmmScatterMemoryRead
from memory.process import CS2


async def player_dot(sio: AsyncClient) -> None:
    player_dot_data = list()
    if CS2.memory_mode == "vmm":
        scatter: VmmScatterMemory = CS2.process.memory.scatter_initialize(FLAG_NOCACHE)

    for player_entity in EntityList.player_entities:
        if not player_entity: continue
        if not player_entity.health: continue

        if CS2.memory_mode == "vmm":
            scatter.clear(FLAG_NOCACHE)

            for fields in (
                    CS2.schemas.client_dll.CBasePlayerController,
                    CS2.schemas.client_dll.CCSPlayerController,
            ):
                fields_value = fields.__dict__.values()
                scatter.prepare(
                    player_entity.controller_address.address + min(fields_value),
                    max(fields_value) - min(fields_value)
                )

            for fields in (
                    CS2.schemas.client_dll.C_BaseEntity,
                    CS2.schemas.client_dll.C_BasePlayerPawn,
                    CS2.schemas.client_dll.C_CSPlayerPawnBase,
            ):
                fields_value = fields.__dict__.values()
                scatter.prepare(
                    player_entity.pawn_address.address + min(fields_value),
                    max(fields_value) - min(fields_value)
                )

            scatter.execute()
            scatter_memory_read = VmmScatterMemoryRead(scatter)
            player_entity = player_entity.get_scatter_mode(scatter_memory_read)

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

    if CS2.memory_mode == "vmm":
        scatter.close()
    if sio.connected:
        # asyncio.create_task(sio.call('player_dot', dict(
        #     t=time(),
        #     players=player_dot_data
        # ), timeout=1))
        await sio.call('player_dot', dict(
            t=time(),
            players=player_dot_data
        ), timeout=1)
