from logging import info, error, warning
from operator import itemgetter
from tomllib import load

# from os import getenv

import socketio
# from discord import Intents, Embed, ui, ButtonStyle, Interaction
# from discord.ext import commands
# from discord.ext.commands import Bot
# from discord.utils import setup_logging
# from dotenv import load_dotenv
import asyncio


from game.entity_list import EntityList
from memory.address import Address
from memory.process import CS2
from runtime.bomb_dot import bomb_dot
from runtime.map_update import map_update
from runtime.player_dot import player_dot
from utils.logger_setup import logger_setup
from utils.memory_monitor import MemoryMonitor


async def socketio_setup() -> socketio.AsyncClient:
    sio = socketio.AsyncClient()

    @sio.event
    def connect() -> None:
        info("🖧Server Connected!")

    @sio.event
    def disconnect() -> None:
        info("🖧Server Disconnected!")

    @sio.event
    async def connected(ip: str) -> None:
        ...
        # msg = Embed()
        # msg.set_author(name="%s 已连接" % ip, icon_url=f"http://122.100.156.26:{getenv("SERVER_PORT")}/static/img/icon.png")
        # await dc.get_channel(int(getenv("TEXT_CHANNEL"))).send(embed=msg)
    server_ip, server_port = itemgetter("server_ip", "server_port")(config)


    await sio.connect(f"http://{server_ip}:{server_port}")
    return sio

# async def discord_setup() -> Bot:
#     intents = Intents.default()
#     intents.members = True
#     intents.message_content = True
#     bot = commands.Bot(command_prefix="|", intents=intents)
#     setup_logging(level=INFO)
#
#     @bot.command()
#     async def hello(ctx):
#         await ctx.send('叫叫叫，叫你妈叫')
#
#     return bot

# async def discord_start(bot: Bot, lock: asyncio.Event) -> None:
#     @bot.event
#     async def on_ready():
#         print("👾%s" % bot.user.name)
#         msg = Embed(title="👾 **DMA，启动！** 👾")
#         msg.set_thumbnail(url=f"http://122.100.156.26:{getenv("SERVER_PORT")}/static/img/icon.png")
#         msg.add_field(name="",
#                       value="[%s](%s)" % ("点击自动下载原神", f"http://122.100.156.26:{getenv("SERVER_PORT")}/"),
#                       inline=False)
#
#         # class MyView(ui.View):
#         #     @ui.button(label='点击下载原神', style=ButtonStyle.blurple)
#         #     async def on_button_click(self, interaction: Interaction, button: ui.Button) -> None:
#         #         await interaction.response.edit_message(content='Button clicked!')
#
#         await bot.get_channel(int(getenv("TEXT_CHANNEL"))).send(embed=msg)  # , view=MyView()
#         lock.set()
#
#     await bot.start(getenv("DISCORD_TOKEN"))
def memory_setup() -> None:
    (
        CS2
        .setup()
        # .dump_offset()
        .load_offset_snapshot("offset_snapshot.pkl")
    )

async def main() -> None:
    # load_dotenv()
    with open("config.toml", "rb") as config_file:
        global config
        config = load(config_file)

    # global dc
    # dc = await discord_setup()
    # lock = asyncio.Event()
    # asyncio.create_task(discord_start(dc, lock))
    # await lock.wait()

    sio = await socketio_setup()

    @sio.on("sync_map_request")
    def sync_map_request() -> dict[str, float | str]:
        return map_update()

    CS2.meow_mode()
    memory_setup()

    async def loop() -> None:
        while True:
            if not sio.connected:
                warning("⚠️ waiting for reconnect, pause 1 sec.")
                await asyncio.sleep(1)
                continue

            try:
                (
                    EntityList
                    .update_entity_list_address()
                    .update_player_entities(True, True)
                )
            except Exception:
                warning("⚠️ EntityList update failed, pause 1 sec.")
                await asyncio.sleep(1)
            else:
                try: await asyncio.gather(
                    player_dot(sio),
                    bomb_dot(sio),
                )
                except Exception as err: error(err)
            # await asyncio.sleep(uniform(0, .2))

            Address.clear_cache()
            MemoryMonitor.reset()

    async def life_check_loop() -> None:
        nonlocal main_loop

        while True:
            is_alive = CS2.is_process_exist()
            if is_alive: await asyncio.sleep(3)
            else:
                main_loop.cancel()
                info("%s dead💥, waiting game start..." % CS2.PROCESS_NAME)

                while not CS2.is_process_exist(): await asyncio.sleep(1)
                while not CS2.is_process_ready(): await asyncio.sleep(1)
                memory_setup()

                main_loop = asyncio.create_task(loop())


    main_loop = asyncio.create_task(loop())
    asyncio.create_task(life_check_loop())
    await sio.wait()



if __name__ == '__main__':
    logger_setup()
    asyncio.run(main())