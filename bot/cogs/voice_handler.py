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

"""
"""

import logging

from discord import Interaction, app_commands
from discord.ext import commands

from bot.utils.config_loader import command_guild_scope


class VoiceHandler(commands.Cog):
    """Handle voice channel connection and commands related to the application.

    Attributes:
        bot: The Discord bot instance this cog is attached to.
    """

    def __init__(self, bot: commands.bot):
        """Initialize the VoiceHandler cog.

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

        self.logger.info("Voice handler is online!")

    @command_guild_scope
    @app_commands.command(
        name="join", description="Bot joins current voice channel"
    )
    async def join(self, interaction: Interaction) -> None:
        """Join the voice channel of the interaction user if the user is
            currently in a voice channel.

        Args:
            interaction (Interaction): Discord command interaction.

        Returns:
            None
        """
        if interaction.user.voice is None:
            await interaction.response.send_message(
                "You are not in a voice channel!", ephemeral=True
            )
            return

        channel = interaction.user.voice.channel
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.move_to(channel)
        else:
            await channel.connect()

        await interaction.response.send_message(
            f"Joined {channel.name}!", silent=True
        )

    @command_guild_scope
    @app_commands.command(
        name="leave", description="Bot leaves current voice channel"
    )
    async def leave(self, interaction: Interaction) -> None:
        """Disconnect the bot from the current voice channel if in one.

        Args:
            interaction (Interaction): Discord command interaction.

        Returns:
            None
        """

        if interaction.guild.voice_client:
            await interaction.response.send_message(
                f"Leaving {interaction.guild.voice_client.channel.name}!",
                silent=True
            )
            await interaction.guild.voice_client.disconnect(force=True)
        else:
            await interaction.response.send_message(
                "Not currently in a voice channel", ephemeral=True
            )


async def setup(bot: commands.Bot) -> None:
    """Load the VoiceHandler cog into the bot.

    Args:
        bot (commands.Bot): The bot instance this cog is attached to.

    Returns:
        None
    """

    await bot.add_cog(VoiceHandler(bot))
