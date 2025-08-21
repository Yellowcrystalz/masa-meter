import discord

from sqlalchemy import Result


class LeaderboardUI(discord.ui.View):
    def __init__(self, results: Result):
        super().__init__()
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
        message = ""

        for i, (username, score) in enumerate(results, start=1):
            message += f"{self.emoji_dict[i]} - {username} - **{score}**\n"

        return message

    async def start(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(
            embed=self.embed,
            view=self
        )
