import discord
from discord import Interaction, Member, app_commands
from discord.ext import commands

from bot.ui.leaderboard_ui import LeaderboardUI
from bot.utils.logger import app_logger

from db.crud import increment_meter, get_leaderboard
from db.database import get_session


class TextHandler(commands.Cog):
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
    async def leaderboard(self, interaction: discord.Interaction):
        with get_session() as session:
            results = get_leaderboard(session)
        leaderboard_ui = LeaderboardUI(results)
        await leaderboard_ui.start(interaction)


async def setup(bot: commands.Bot):
    await bot.add_cog(TextHandler(bot))
