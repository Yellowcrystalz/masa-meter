import asyncio
import signal

import discord
from discord.ext import commands, tasks

from config import DISCORD_TOKEN, COGS_DIR
from bot.logger import app_logger
from db.crud import get_meter
from db.database import get_session


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="mm ", intents=intents)


@tasks.loop(seconds=5)
async def update_bot_status():
    with get_session() as session:
        count = get_meter(session)

    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name=f"Sushi Masa Count: {count}"
    ))


@bot.event
async def on_ready():
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
async def shutdown(ctx):
    app_logger.info("Masa-Meter is shutting down!")
    await ctx.send("shutting down!")
    await bot.close()


async def load():
    for file in COGS_DIR.iterdir():
        if file.suffix == ".py" and file.stem != "__init__":
            await bot.load_extension(f"bot.cogs.{file.stem}")


async def shutdown_signal():
    app_logger.info("Masa-Meter is shutting down!")
    await bot.close()


async def main():
    loop = asyncio.get_running_loop()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown_signal()))

    async with bot:
        await load()
        await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
