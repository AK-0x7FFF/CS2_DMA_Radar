from json import load
from os import getenv
from time import time

import socketio
from dotenv import load_dotenv
import asyncio

from game.entity_list import EntityList
from memory.address import Address
from memory.process import CS2
from runtime.bomb_dot import bomb_dot
from runtime.map_update import map_update
from runtime.player_dot import player_dot
from utils.memory_monitor import MemoryMonitor


async def socketio_setup() -> socketio.AsyncClient:
    sio = socketio.AsyncClient()

    @sio.event
    def connect() -> None:
        print("Server Connected.")

    @sio.event
    def disconnect() -> None:
        print("Server Disconnected.")

    await sio.connect('http://127.0.0.1:1090')
    return sio


async def main() -> None:
    load_dotenv()

    @lambda func: func()
    def setup() -> None:
        (
            CS2
            .meow_mode()
            .setup()
            # .dump_offset()
            .load_offset_snapshot("offset_snapshot.pkl")
        )

    sio = await socketio_setup()

    @sio.on("sync_map_request")
    def sync_map_request() -> dict[str, float | str]:
        return map_update()


    async def loop():
        while True:
            if not sio.connected:
                print("waiting for reconnect")
                await asyncio.sleep(1)
                continue

            try:
                (
                    EntityList
                    .update_entity_list_address()
                    .update_player_entities(False, False)
                )
            except Exception:
                print("EntityList update failed, pause 1 sec.")
                await asyncio.sleep(1)
            else:
                try: await asyncio.gather(
                    player_dot(sio),
                    bomb_dot(sio),
                )
                except Exception as error: print("error", error)

            Address.clear_cache()
            MemoryMonitor.reset()

    asyncio.create_task(loop())
    await sio.wait()



if __name__ == '__main__':
    asyncio.run(main())