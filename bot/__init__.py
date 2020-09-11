import os

from discord.ext import commands

from .cogs.timer import Timer
from .cogs.kanzler import Kanzler


class Bot(commands.Bot):
    def __init__(self) -> None:
        command_prefix = os.getenv("COMMAND_PREFIX")

        super().__init__(command_prefix=command_prefix)

        # Add cogs
        self.add_cog(Timer(self))
        self.add_cog(Kanzler(self))

    async def on_ready(self) -> None:
        print("Bot started")
