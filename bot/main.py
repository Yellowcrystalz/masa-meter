import discord
from discord.ext import commands

from dotenv import load_dotenv

import asyncio
import logging
import os


load_dotenv(dotenv_path="../.env")
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="mm ", intents=intents)


@bot.event
async def on_ready():
    print("Ready!")

    try:
        synced_commands = await bot.tree.sync()
        if len(synced_commands) == 1:
            print("Synced 1 command.")
        else:
            print(f"Synced {len(synced_commands)} commands.")
    except Exception as e:
        print("An error with syncing application commands has occured: ", e)


@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("shutting down!")
    await bot.close()


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')


async def main():
    async with bot:
        await load()
        await bot.start(token, log_handler=handler, log_level=logging.DEBUG)


if __name__ == "__main__":
    asyncio.run(main())
