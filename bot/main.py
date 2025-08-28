"""
Masa Meter Discord Bot

This bot tracks and displays the current Sushi Masa Meter as its Discord presence (status).
It connect to a database to fetch meter values, and supports incrementing the Sushi Masa Meter
through the bot.

Enviroment:
    By default, the bot runs in testing mode using the test token.
    To run in production mode, use one of the following flags:
        -p
        --prod
        --production

Run with:
    # Run in testing mode(default)
    python -m bot.main

    # Run in production mode
    python -m bot.main --prod
"""

import asyncio
import signal

import discord
from discord.ext import commands, tasks

from config import COGS_DIR
from bot.utils.config_loader import get_token
from bot.utils.logger import app_logger
from db.crud import get_meter
from db.database import get_session


# Loads production token if -p, --prod, or --prodution is passed, otherwises loads test token
TOKEN = get_token()

# Configures the Discord bot with the proper intents and sets commands prefix to mm
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="mm ", intents=intents)


@tasks.loop(seconds=5)
async def update_bot_status() -> None:
    """
    Periodically updates the bot's Discord status to reflect the Sushi Masa Meter.

    Runs every 5 seconds:
    - Retrieves the meter from the database.
    - Updates the bot's presence (Discord status) with the retrieved meter value.
    """

    with get_session() as session:
        meter = get_meter(session)  # Fetch the current meter value from database

    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name=f"Sushi Masa Meter: {meter}"
    ))


@bot.event
async def on_ready() -> None:
    """
    Event handler trigged when the bot successfully connects to Discord's API.

    - Logs the connection when successful.
    - Starts a background task for updating the bot's status.
    - Attempts to sync application (slash) commands with Discord.
    """

    app_logger.info("Masa-Meter is connected to Discord!")
    update_bot_status.start()

    try:
        synced_commands = await bot.tree.sync()
        if len(synced_commands) == 1:
            app_logger.info("Synced 1 command.")
        else:
            app_logger.info(f"Synced {len(synced_commands)} commands.")
    except Exception as e:
        app_logger.exception("An error with syncing application commands has occured: %s", e)


@bot.command()
@commands.is_owner()
async def shutdown(ctx: commands.Context) -> None:
    """
    Shuts down the bot safely. (Owner-only command)

    Usage:
        mm shutdown

    Args:
        ctx (commands.Context): The context of the command invocation.
    """

    app_logger.info("Masa-Meter is shutting down!")
    await ctx.send("shutting down!")
    await bot.close()


async def load() -> None:
    """
    Dynamically loads all cogs from the cogs directory.

    - Loads each Python file (except __init__.py) as a bot extension.
    """

    for file in COGS_DIR.iterdir():
        if file.suffix == ".py" and file.stem != "__init__":
            await bot.load_extension(f"bot.cogs.{file.stem}")


async def shutdown_signal() -> None:
    """
    Gracefully shuts down the bot in interrupt or termination cases.

    - Called when recieving SIGINT (CTRL+C) or SIGTERM (TERMINATION).

    This function was introduced to ensure proper shutdown behavior when running alongside the web
    application so both services can terminate gracefully when sent a SIGINT.
    """

    app_logger.info("Masa-Meter is shutting down!")
    await bot.close()


async def main() -> None:
    """
    Entry point for running the Discord bot.

    - Starts signal handler for shutdown.
    - Dynamically loads the cogs.
    - Starts the bot with the configured token.
    """

    loop = asyncio.get_running_loop()

    # Listens for SIGINT or SIGTERM to execute a graceful shutdown
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown_signal()))

    async with bot:
        await load()
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
