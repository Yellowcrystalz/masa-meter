from contextlib import contextmanager

import discord
from discord import Interaction, Member, app_commands
from discord.ext import commands

from bot.logger import app_logger

from db.crud import *
from db.database import SessionLocal
from db.models import User, Report


@contextmanager
def get_session():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


class MasaMeter(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = app_logger

    @commands.Cog.listener()
    async def on_ready(self):
        print("Masa-Meter is online!")
        self.logger.info("Masa-Meter is online!")

    @app_commands.command(name="increment", description="Increments the Masa Meter")
    async def increment(self, interaction: Interaction, offender: Member):
        print(interaction.user)

    @app_commands.command(name="leaderboard", description="Shows the Leaderboard")
    async def history(self, interaction: discord.Interaction):
        await interaction.response.send_message("doesn't work yet")


async def setup(bot: commands.Bot):
    await bot.add_cog(MasaMeter(bot))
