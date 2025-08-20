import asyncio

import discord
from discord.ext import commands

from config import DISCORD_TOKEN, COGS_DIR
from bot.logger import app_logger


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="mm ", intents=intents)


@bot.event
async def on_ready():
    app_logger.info("Masa-Meter is connected to Discord!")

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


async def main():
    async with bot:
        await load()
        await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
