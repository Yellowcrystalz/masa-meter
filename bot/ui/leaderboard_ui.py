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

"""Render a Discord leaderboard UI with results from a SQLAlchemy query.

Format the top five usernames and scores from a SQLAlchemy Result object into a
Discord embed with medal emojis representing the place. Provide a Discord UI
view that can show the leaderboard in response to an interaction.
"""

import discord

from sqlalchemy import Result


class LeaderboardUI(discord.ui.View):
    """Generate a Discord UI view containing a leaderboard of the top five
        speakers with the most mentions.

    Attributes:
        emoji_dict:
            A dict that maps the discord medal to its corresponding number.
            Numbers 4 and 5 are mapped to the normal medal emoji
        embed:
            A Discord embed containing the contents of the leaderboard.
    """

    def __init__(self, results: Result):
        """Initialize the leaderboard view.

        Args:
            results:
                A SQLAlchemy Result object containing the leaderboard
                (username, score).
        """

        super().__init__()

        # Discord medal emojis stored in a dictionary
        self.emoji_dict: dict[int, str] = {
            1: ":first_place:",
            2: ":second_place:",
            3: ":third_place:",
            4: ":medal:",
            5: ":medal:"
        }

        self.embed: discord.embed = discord.Embed(
            title="Masa Meter Leaderboard"
        )

        self.embed.add_field(
            name="",
            value=self.results_to_embed(results)
        )

    def results_to_embed(self, results: Result) -> str:
        """Convert top 5 leaderboard results into a formatted embed.

        Args:
            results:
                A SQLAlchemy Result object containing the leaderboard
                (username, score).

        Returns:
            A formatted string (embed) with up to the top 5 leaderboard entries.
        """

        message: str = ""

        # We used string concatenation to build the embeded message by iterating
        # through results.

        for i, (username, score) in enumerate(results, start=1):
            if i > 5:
                break

            message += f"{self.emoji_dict[i]} - {username} - **{score}**\n"

        return message

    async def start(self, interaction: discord.Interaction) -> None:
        """Send the leaderboard as a response to an interaction.

        Args:
            interaction: A Discord command interaction.

        Returns:
            None
        """

        await interaction.response.send_message(
            embed=self.embed,
            view=self,
            silent=True
        )
