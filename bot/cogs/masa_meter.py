import discord
from discord import Interaction, Member, app_commands
from discord.ext import commands

from bot.logger import app_logger

from db.crud import increment_meter
from db.database import get_session


class MasaMeter(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = app_logger

    @commands.Cog.listener()
    async def on_ready(self):
        print("Masa-Meter is online!")
        self.logger.info("Masa-Meter is online!")

    @app_commands.command(name="increment", description="Increments the Masa Meter")
    @app_commands.describe(speaker="Person who said Sushi Masa")
    async def increment(self, interaction: Interaction, speaker: Member):
        with get_session() as session:
            increment_meter(session, speaker.name)
        await interaction.response.send_message("Masa Meter has gone up!")

    @app_commands.command(name="leaderboard", description="Shows the Leaderboard")
    async def history(self, interaction: discord.Interaction):
        await interaction.response.send_message("doesn't work yet")


async def setup(bot: commands.Bot):
    await bot.add_cog(MasaMeter(bot))
