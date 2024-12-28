import asyncio
from time import time

from socketio import AsyncClient

from game.planted_c4_entity import PlantedC4
from memory.process import CS2


async def bomb_dot(sio: AsyncClient) -> None:
    game_rule_address = CS2.signatures.client.dwGameRules.copy().pointer()
    is_c4_planted = game_rule_address.copy().offset(CS2.schemas.client_dll.C_CSGameRules.m_bBombPlanted).bool()

    if not is_c4_planted:
        if sio.connected:
            await sio.call('bomb_dot', dict(
                t=time(),
                planted=False,
                bomb=None
            ), timeout=1)
        return

    planted_c4 = PlantedC4(CS2.signatures.client.dwPlantedC4.copy().pointer().pointer())
    if (pos := planted_c4.pos) is None: return
    # if (site := planted_c4.site) is not None: return

    if sio.connected:
        await sio.call('bomb_dot', dict(
            t=time(),
            planted=True,
            bomb=dict(
                pos=pos.__dict__,
            ),
        ), timeout=1)
