# MIT License
#
# Copyright (c) 2025 Justin Nguyen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Tracks and displays the current Sushi Masa Meter as the bot's Discord
    presence (status).

Connects to a database to fetch meter values, and supports incrementing the
Sushi Masa Meter through commands.

Examples:
    Run in testing mode (default):
        python -m bot.main

    Run in production mode:
        python -m bot.main -p
        python -m bot.main --prod
        python -m bot.main --production
"""

import asyncio
import signal

import discord
from discord.ext import commands, tasks

from config import COGS_DIR

from bot.utils.config_loader import BOT_TOKEN, tree_sync
from bot.utils.logger import app_logger

from db.crud import get_meter
from db.database import get_session


class MasaBot(commands.Bot):
    """
    """

    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def on_ready(self) -> None:
        """Log bot connection and start the background status update task.

        Returns:
            None
        """

        app_logger.info("Masa Meter is connected to Discord!")
        self.update_bot_status.start()

        await tree_sync(self.tree)

        app_logger.info("Masa Meter is ready!")

    async def shutdown(self) -> None:
        """Shut down the bot "safely" and logs it.

        Returns:
            None
        """

        app_logger.info("Masa Meter is shutting down!")
        await self.close()

    async def load_cogs(self) -> None:
        """Load all bot cogs from the cogs directory.

        Returns:
            None
        """

        for file in COGS_DIR.iterdir():
            if file.suffix == ".py" and file.stem != "__init__":
                await self.load_extension(f"bot.cogs.{file.stem}")
                app_logger.info(f"Loaded {file}")

    async def reload_cogs(self) -> None:
        """Reload all cogs to reflect file changes.

        Returns:
            None
        """

        try:
            for ext in list(self.extensions.keys()):
                await self.unload_extension(ext)

            await self.load_cogs()
        except Exception:
            raise

    @tasks.loop(seconds=5)
    async def update_bot_status(self) -> None:
        """Update the bot's Discord status with the current Sushi Masa Meter

        Returns:
            None
        """

        # Polling every 5 seconds to avoid complex event-driven logic.

        with get_session() as session:
            meter: int = get_meter(session)

        await self.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"Sushi Masa Meter: {meter}"
        ))


async def main() -> None:
    """Run the Discord bot and register signal handlers for graceful shutdown.

    Set up intents for Discord bot to run properly.

    Returns:
        None
    """

    intents: discord.Intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True
    bot: MasaBot = MasaBot(command_prefix="mm", intents=intents)

    loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()

    # Listens for SIGINT or SIGTERM to execute a graceful shutdown.
    # Used to sync up program termination with web app side of application.

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(
            sig,
            lambda: asyncio.create_task(bot.shutdown())
        )

    async with bot:
        await bot.load_cogs()
        await bot.start(BOT_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
