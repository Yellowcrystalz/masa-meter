"""
Leaderboard UI

This module defines the LeaderboardUI, a Discord UI view that displays the Masa Meter leaderboard
in an embed for the top 5 users.
"""

import discord

from sqlalchemy import Result


class LeaderboardUI(discord.ui.View):
    """
    A Discord UI view for display the Masa Meter leaderboard.

    - The top 5 users are displayed in embedded message.
    """

    def __init__(self, results: Result):
        """
        Initialize the leaderboard view.

        - Contains an embed attribute
        - Contains a dict to store Discord medal emojis

        Args:
            results (Result): A SQLAlchemy Result object containing the leaderboard
                (username, score).
        """

        super().__init__()

        # Discord medal emojis stored in a dictionary
        self.emoji_dict = {
            1: ":first_place:",
            2: ":second_place:",
            3: ":third_place:",
            4: ":medal:",
            5: ":medal:"
        }
        self.embed = discord.Embed(title="Masa Meter Leaderboard")
        self.embed.add_field(
            name="",
            value=self.results_to_embed(results)
        )

    def results_to_embed(self, results: Result) -> str:
        """
        Convert leaderboard results into a formatted embed.

        - Creates a formatted string for each entry.
        - Combines the top 5 entries into one string.

        Args:
            results (Result): A SQLAlchemy Result object containing the leaderboard
                (username, score).

        Returns:
            str: A formatted string (embed) with up to the top 5 leaderboard entries.
        """

        message = ""

        for i, (username, score) in enumerate(results, start=1):
            if i > 5:
                break

            message += f"{self.emoji_dict[i]} - {username} - **{score}**\n"

        return message

    async def start(self, interaction: discord.Interaction) -> None:
        """
        Sends the leaderboard as a response to an interaction.

        - Sends the view and the embed to the user.

        Args:
            interaction (discord.Interaction): Discord command interaction.
        """

        await interaction.response.send_message(
            embed=self.embed,
            view=self
        )
