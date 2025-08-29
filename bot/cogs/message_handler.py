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

"""Handle user messages and slash commands for incrementing the Masa Meter.

Detect for variations of the phrase "Sushi Masa" in text channels and increments
the meter when a match occurs. Provides a slash command to manually increment
the meter for a specified user and to display the leaderboard with a custom UI
"""

import logging
import re

import discord
from discord import Interaction, Member, Message, app_commands
from discord.ext import commands

from sqlalchemy import Result

from bot.ui.leaderboard_ui import LeaderboardUI

from db.crud import increment_meter, get_leaderboard
from db.database import get_session


class MessageHandler(commands.Cog):
    """Responsible for handling chat messages and commands related to the
        application.

    Attributes:
        bot: The Discord bot instance this cog is attached to.
    """

    def __init__(self, bot: commands.Bot):
        """
        Initialize the MessageHandler cog.

        Args:
            bot : Defines the Discord bot instance this cog is attached to.
        """

        self.bot: commands.Bot = bot
        self.logger: logging.Logger = logging.getLogger(__name__)

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """Log when this cog is succesfully loaded.

        Returns:
            None
        """

        self.logger.info("Message handler is online!")

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        """ Detects variations of "Sushi Masa" in messages and increments the
            meter.

        Ignores messages sent by the bot itself. Increments the meter when a
        match is found and replies to confirm.

        Args:
            message: Discord message object retrieved from the text channel.

        Returns:
            None
        """

        if message.author == self.bot.user:
            return

        # Regex to search for numerous variations of "Sushi Masa" in a message.
        expr: str = (
            r"\b[s$5z]+\s*[uv]+\s*[s$5z]+\s*[h#4]+\s*[i1!l]+"    # Sushi regex
            r"\s*(m|nn)+\s*[a@4]+\s*[s$5z]+\s*[a@4]+(\b|$|\s*)"  # Masa regex
        )
        pattern: re.Pattern = re.compile(expr, re.I)

        if pattern.search(message.content):
            with get_session() as session:
                increment_meter(session, message.author.name)

            self.logger.info(f"{message.author.name} said Sushi Masa")
            await message.reply("Masa Meter has gone up!")

    @app_commands.command(
        name="increment", description="Increments the Masa Meter"
    )
    @app_commands.describe(speaker="Person who said Sushi Masa")
    async def increment(
        self, interaction: Interaction, speaker: Member
    ) -> None:
        """Increments the meter manually for a specified user.

        Connects with the database, increments the meter, and replies to confirm
        the increment.

        Args:
            interaction: Discord command interaction.
            speaker: Username of the one responsible for saying "Sushi Masa".

        Returns:
            None
        """

        with get_session() as session:
            increment_meter(session, speaker.name)

        self.logger.info(f"{speaker.name} said Sushi Masa")
        await interaction.response.send_message("Masa Meter has gone up!")

    @app_commands.command(
        name="leaderboard", description="Shows the Leaderboard"
    )
    async def leaderboard(self, interaction: Interaction) -> None:
        """Display the Masa Meter leaderboard.

        Fetch leaderboard data from the database and start the leaderboard UI.

        Args:
            interaction (Interaction): Discord command interaction.

        Returns:
            None
        """

        with get_session() as session:
            results: Result = get_leaderboard(session)

        leaderboard_ui: discord.ui.View = LeaderboardUI(results)

        self.logger.info(
            f"{interaction.user.name} used the leaderboard command"
        )

        await leaderboard_ui.start(interaction)


async def setup(bot: commands.Bot) -> None:
    """Loads the MessageHandler cog into the bot.

    Args:
        bot (commands.Bot): The bot instance this cog is attached to.

    Returns:
        None
    """

    await bot.add_cog(MessageHandler(bot))
