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
the meter for a specified user and to display the leaderboard with a custom UI.
"""

import logging
import re

from discord import ApplicationContext, Member, Message, Option, slash_command
from discord.ui import View
from discord.ext import commands

from sqlalchemy import Result

from bot.main import MasaBot
from bot.ui.help_ui import HelpUI
from bot.ui.info_ui import InfoUI
from bot.ui.leaderboard_ui import LeaderboardUI
from bot.utils.config_loader import GUILD_ID_LIST

from db.crud import create_mention, get_leaderboard
from db.database import get_session


class MessageHandler(commands.Cog):
    """Handele chat messages and commands related to the
        application.

    Attributes:
        bot: The Discord bot instance this cog is attached to.
        logger: Logger object that logs events from this cog.
    """

    def __init__(self, bot: MasaBot):
        """Initialize the MessageHandler cog.

        Args:
            bot : Defines the Discord bot instance this cog is attached to.
        """

        self.bot: MasaBot = bot
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
            r"[s$5z]+[\s_-]*[uv]+[\s_-]*[s$5z]+[\s_-]*[h#4]+[\s_-]*[i1!l]+"
            r"[\s\S]*"
            r"m+[\s_-]*[a@4]+[\s_-]*[s$5z]+[\s_-]*[a@4]+"
        )
        pattern: re.Pattern = re.compile(expr, re.I)

        if pattern.search(message.content):
            with get_session() as session:
                create_mention(session, message.author.name)

            self.logger.info(f"{message.author.name} said Sushi Masa")
            await message.reply("Masa Meter has gone up!")

    @slash_command(
        name="help",
        description="Show Masa Meter commands",
        guild_ids=GUILD_ID_LIST
    )
    async def help(self, ctx: ApplicationContext) -> None:
        """Show all the avaiable bot slash commands.

        Args:
            interaction: Discord command interaction.

        Returns:
            None
        """

        help_ui: View = HelpUI()

        await help_ui.start(ctx)

    @slash_command(
        name="info",
        description="Shows info about the bot",
        guild_ids=GUILD_ID_LIST
    )
    async def info(self, ctx: ApplicationContext) -> None:
        """Show information about the bot, including description and useful
        links

        Args:
            interaction: Discord command interaction.

        Returns:
            None
        """

        info_ui: View = InfoUI()

        await info_ui.start(ctx)

    @slash_command(
        name="increment",
        description="Increments the Masa Meter",
        guild_ids=GUILD_ID_LIST
    )
    async def increment(
        self,
        ctx: ApplicationContext,
        speaker=Option(Member, "Person who said Sushi Masa")
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
            create_mention(session, speaker.name)

        self.logger.info(f"{speaker.name} said Sushi Masa")
        await ctx.respond("Masa Meter has gone up!")

    @slash_command(
        name="leaderboard",
        description="Shows the leaderboard",
        guild_ids=GUILD_ID_LIST
    )
    async def leaderboard(self, ctx: ApplicationContext) -> None:
        """Display the Masa Meter leaderboard.

        Fetch leaderboard data from the database and start the leaderboard UI.

        Args:
            interaction (Interaction): Discord command interaction.

        Returns:
            None
        """

        with get_session() as session:
            results: Result = get_leaderboard(session)

        leaderboard_ui: View = LeaderboardUI(results)

        self.logger.info(
            f"{ctx.author.name} used the leaderboard command"
        )

        await leaderboard_ui.start(ctx)


def setup(bot: commands.Bot) -> None:
    """Load the VoiceHandler cog into the bot.

    Args:
        bot (commands.Bot): The bot instance this cog is attached to.

    Returns:
        None
    """

    bot.add_cog(MessageHandler(bot))
