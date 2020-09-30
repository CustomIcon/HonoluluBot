from os import environ
from configparser import ConfigParser
from pyrogram import Client


API_ID = environ.get('API_ID', None)
API_HASH = environ.get('API_HASH', None)
BOT_SESSION = environ.get('BOT_SESSION', None)


class honolulubot(Client):
    def __init__(self, name):
        name = name.lower()
        config_file = f"{name}.ini"

        config = ConfigParser()
        config.read(config_file)

        plugins = dict(root=f"{name}.plugins", )

        super().__init__(
            BOT_SESSION if BOT_SESSION is not None else name,
            api_id=API_ID,
            api_hash=API_HASH,
            config_file=config_file,
            workers=16,
            plugins=plugins,
            workdir="./",
            app_version="honolulubot v1.1",
        )

    async def start(self):
        await super().start()
        print("Bot started. Hi.")

    async def stop(self, *args):
        await super().stop()
        print("Bot stopped. Bye.")
