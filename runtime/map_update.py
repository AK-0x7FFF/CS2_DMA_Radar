import asyncio
from time import time

from socketio import AsyncClient

from memory.process import CS2


def map_update() -> dict[str, float | str]:
    global_var_address = CS2.signatures.client.dwGlobalVars.copy().pointer()

    try:
        map_name_address = global_var_address.offset(0x180).pointer()
        map_name = map_name_address.str(50)
    except Exception:
        map_name = "<empty>"

    return dict(
            t=time(),
            map_name=map_name
        )