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

from bot.utils.config_loader import BOT_TOKEN
from bot.utils.logger import app_logger
from db.crud import get_meter
from db.database import get_session


intents: discord.Intents = discord.Intents.default()
intents.message_content = True
bot: commands.Bot = commands.Bot(command_prefix="mm ", intents=intents)


@tasks.loop(seconds=5)
async def update_bot_status() -> None:
    """ Update the bot's Discord status with the current Sushi Masa Meter

    Returns:
        None
    """

    # Polling every 5 seconds to avoid complex event-driven logic.

    with get_session() as session:
        meter: int = get_meter(session)

    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name=f"Sushi Masa Meter: {meter}"
    ))


@bot.event
async def on_ready() -> None:
    """Log bot connection and start the background status update task.

    Returns:
        None
    """

    app_logger.info("Masa-Meter is connected to Discord!")
    update_bot_status.start()

    try:
        synced_commands: list = await bot.tree.sync()
        if len(synced_commands) == 1:
            app_logger.info("Synced 1 command.")
        else:
            app_logger.info(f"Synced {len(synced_commands)} commands.")
    except Exception as e:
        app_logger.exception(
            "An error with syncing application commands has occured: %s",
            e
        )


@bot.command()
@commands.is_owner()
async def shutdown(ctx: commands.Context) -> None:
    """Shuts down the bot safely. (Owner-only command)

    Args:
        ctx (commands.Context): Context of the command invocation.

    Returns:
        None

    Examples:
        mm shutdown

    """

    app_logger.info("Masa-Meter is shutting down!")
    await ctx.send("shutting down!")
    await bot.close()


async def load() -> None:
    """Load all bot cogs from the cogs directory.

    Returns:
        None
    """

    # Dynamically loading cogs from the cogs directory into the bot.

    for file in COGS_DIR.iterdir():
        if file.suffix == ".py" and file.stem != "__init__":
            await bot.load_extension(f"bot.cogs.{file.stem}")


async def shutdown_signal() -> None:
    """Handle SIGINT or SIGTERM and shut down the bot gracefully.


    Returns:
        None
    """

    app_logger.info("Masa-Meter is shutting down!")
    await bot.close()


async def main() -> None:
    """ Run the Discord bot and register signal handlers for graceful shutdown.

    Returns:
        None
    """

    loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()

    # Listens for SIGINT or SIGTERM to execute a graceful shutdown.
    # Used to sync up program termination with web app side of application.

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(
            sig,
            lambda: asyncio.create_task(shutdown_signal())
        )

    async with bot:
        await load()
        await bot.start(BOT_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
