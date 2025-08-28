"""
Message Handler Cog

This cog handles user messages and slash commands for incrementing the Sushi Masa Meter.

Features:
    - Listens for variations of the phrase "Sushi Masa" in text channels and increments the
        meter when a match is made.
    - Provides a slash command to manually increment the meter for a specified user.
    - Provides a slash command to display the leaderboard with a custom UI
"""

import logging
import re

from discord import Interaction, Member, Message, app_commands
from discord.ext import commands

from bot.ui.leaderboard_ui import LeaderboardUI

from db.crud import increment_meter, get_leaderboard
from db.database import get_session


class MessageHandler(commands.Cog):
    """
    A Discord cog responsible for handling messages and commandes related to the application.
    """

    def __init__(self, bot: commands.Bot):
        """
        Initialize the MessageHandler cog.

        - Creates a logger with the same namespace as the cog.

        Args:
            bot (commands.Bot): The bot instance this cog is attached to.
        """

        self.bot = bot
        self.logger = logging.getLogger(__name__)

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """
        Event listener triggered when this cog is succesfully loaded.

        - Logs whenever the cog is loaded.
        """

        self.logger.info("Message handler is online!")

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        """
        Event listener for new messages sent in channels the bot can view.

        - Ignores messages sent by the bot itself.
        - Detects variations of "Sushi Masa" using regex.
        - Increments the database meter when a match is made.
        - Replies to confirm the increment.

        Args:
            message (Message): Discord message object retrieved from the text channel.
        """

        if message.author == self.bot.user:
            return

        # Regex to search for numerous variations of "Sushi Masa" in a message.
        expr = r"\b[s$5z]+\s*[uv]+\s*[s$5z]+\s*[h#4]+\s*[i1!l]+\s*(m|nn)+\s*[a@4]+\s*[s$5z]+\s*[a@4]+(\b|$|\s*)"
        pattern = re.compile(expr, re.I)

        if pattern.search(message.content):
            with get_session() as session:
                increment_meter(session, message.author.name)

            self.logger.info(f"{message.author.name} said Sushi Masa")
            await message.reply("Masa Meter has gone up!")

    @app_commands.command(name="increment", description="Increments the Masa Meter")
    @app_commands.describe(speaker="Person who said Sushi Masa")
    async def increment(self, interaction: Interaction, speaker: Member) -> None:
        """
        Application (Slash) command to manually increment the database meter for a given member.

        - Connects with the database and increments the meter
        - Replies to confirm the increment.

        Args:
            interaction (Interaction): Discord command interaction.
            speaker (Member): Username of the one responsible for saying "Sushi Masa".

        """

        with get_session() as session:
            increment_meter(session, speaker.name)

        self.logger.info(f"{speaker.name} said Sushi Masa")
        await interaction.response.send_message("Masa Meter has gone up!")

    @app_commands.command(name="leaderboard", description="Shows the Leaderboard")
    async def leaderboard(self, interaction: Interaction) -> None:
        """
        Application (Slash) command to display the Masa Meter leaderboard.

        - Fetches leaderboard data from the database.
        - Displays the leaderboard with a custom UI.

        Args:
            interaction (Interaction): Discord command interaction.
        """

        with get_session() as session:
            results = get_leaderboard(session)

        leaderboard_ui = LeaderboardUI(results)
        self.logger.info(f"{interaction.user.name} used the leaderboard command")
        await leaderboard_ui.start(interaction)


async def setup(bot: commands.Bot) -> None:
    """
    Set up to load the MessageHandler cog into the bot.

    Args:
        bot (commands.Bot): The bot instance this cog is attached to.
    """

    await bot.add_cog(MessageHandler(bot))
