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

"""Render a Discord UI containing a description of the bot and hyperlinks to a
web dashboard and GitHub repository.
"""

import discord


class InfoUI(discord.ui.View):
    def __init__(self):
        """Generate a Discord info UI with a description of the bot and links to
        the website and github repo.

        Attributes:
            embed: A Discord embed containing a bot description and links.
        """

        super().__init__()

        self.embed: discord.embed = discord.Embed(
            title="Masa Meter Info",
            description=(
                "Bot to track how many times my friends say \"Sushi Masa\""
            )
        )
        self.embed.add_field(
            name="",
            value=(
                "[Website](https://masameter.xyz/)\n"
                "[Github Repo](https://github.com/Yellowcrystalz/masa-meter)"
            ),
            inline=False
        )

    async def start(self, interaction: discord.Interaction) -> None:
        """Send the leaderboard as a response to an interaction.

        Args:
            interaction: A Discord command interaction.

        Returns:
            None
        """

        await interaction.response.send_message(
            embed=self.embed,
            view=self
        )
