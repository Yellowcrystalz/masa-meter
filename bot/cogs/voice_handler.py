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

"""Handle voice related functionality for the Discord bot.

Provide slash commands for joining and leaving the user's current voice channel.
Play a join and leave sound clip.
"""

import logging

from discord import (
    ApplicationContext, FFmpegPCMAudio, PCMVolumeTransformer, VoiceClient,
    slash_command
)
from discord.ext import commands

from config import JOIN_MP3_PATH, LEAVE_MP3_PATH

from bot.main import MasaBot
from bot.utils.config_loader import GUILD_ID_LIST


class VoiceHandler(commands.Cog):
    """Handle voice channel connection and commands related to the application.

    Attributes:
        bot: The Discord bot instance this cog is attached to.
        logger: Logger object that logs events from this cog.
    """

    def __init__(self, bot: MasaBot):
        """Initialize the VoiceHandler cog.

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

        self.logger.info("Voice handler is online!")

    @slash_command(
        name="join",
        description="Bot joins current voice channel",
        guild_ids=GUILD_ID_LIST
    )
    async def join(self, ctx: ApplicationContext) -> None:
        """Join the voice channel of the interaction user if the user is
            currently in a voice channel.

        Args:
            interaction (Interaction): Discord command interaction.

        Returns:
            None
        """
        if ctx.author.voice is None:
            await ctx.respond(
                "You are not in a voice channel!", ephemeral=True
            )
            return

        channel = ctx.author.voice.channel
        voice_client: VoiceClient = ctx.voice_client

        if voice_client:
            await voice_client.disconnect(force=True)

        voice_client = await channel.connect()

        source = PCMVolumeTransformer(
            FFmpegPCMAudio(JOIN_MP3_PATH)
        )
        voice_client.play(
            source,
            after=lambda e: print(f"Player error: {e}") if e else None
        )

        await ctx.respond(f"Joined {channel.name}!")

    @slash_command(
        name="leave",
        description="Bot leaves current voice channel",
        guild_ids=GUILD_ID_LIST
    )
    async def leave(self, ctx: ApplicationContext) -> None:
        """Disconnect the bot from the current voice channel if in one.

        Args:
            interaction (Interaction): Discord command interaction.

        Returns:
            None
        """

        voice_client: VoiceClient = ctx.voice_client

        if voice_client:
            await ctx.respond(f"Leaving {voice_client.channel.name}!")

            source = PCMVolumeTransformer(
                FFmpegPCMAudio(LEAVE_MP3_PATH)
            )
            await voice_client.play(
                source=source,
                after=lambda e: print(f"Player error: {e}") if e else None,
                wait_finish=True
            )

            await voice_client.disconnect(force=False)
        else:
            await ctx.respond(
                "Not currently in a voice channel", ephemeral=True
            )

    @join.before_invoke
    @leave.before_invoke
    async def ensure_voice(self, ctx: ApplicationContext):
        """
        """

        vc = ctx.voice_client

        if vc is not None and vc.is_playing():
            ctx.voice_client.stop()


def setup(bot: commands.Bot) -> None:
    """Load the VoiceHandler cog into the bot.

    Args:
        bot (commands.Bot): The bot instance this cog is attached to.

    Returns:
        None
    """

    bot.add_cog(VoiceHandler(bot))
