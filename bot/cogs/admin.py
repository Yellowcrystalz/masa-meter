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

"""Handle admin commands relating the Discord bot.

Provides slash commands for shutting down the bot and reloading the bot for
files changes inside cog extensions so developers do not have to shut down the
bot.
"""

import logging

from discord import ApplicationContext, slash_command
from discord.ext import commands

from config import DEV_GUILD_ID

from bot.main import MasaBot


class Admin(commands.Cog):
    """Handle admin commands such as shutting down the bot and reloading the bot

    Attributes:
        bot: The Discord bot instance this cog is attached to.
        logger: Logger object that logs events from this cog.
    """

    def __init__(self, bot: MasaBot):
        self.bot: MasaBot = bot
        self.logger: logging.Logger = logging.getLogger(__name__)

    @slash_command(
        name="shutdown",
        description="Shutdown the bot (owner only)",
        guild_ids=[DEV_GUILD_ID]
    )
    @commands.is_owner()
    async def shutdown(self, ctx: ApplicationContext) -> None:
        """Shut down the bot safely. (Owner-only command)

        Args:
            ctx (commands.Context): Context of the command invocation.

        Returns:
            None

        Examples:
            /shutdown
        """

        await ctx.respond("Masa Meter is shutting down!", ephemeral=True)
        await self.bot.shutdown()

    @slash_command(
        name="reload",
        description="Reload the bot (owner only)",
        guild_ids=[DEV_GUILD_ID]
    )
    @commands.is_owner()
    async def reload(self, ctx: ApplicationContext) -> None:
        """Reload the bot for file changes. (Owner-only command)

        Args:
            ctx: Context of the command invocation.

        Returns:
            None

        Examples:
            /reload
        """

        try:
            self.bot.reload_cogs()
            self.logger.info("Masa Meter has reloaded all cogs!")
            await ctx.respond(
                "Masa Meter has reloaded all cogs!", ephemeral=True
            )
        except Exception as e:
            self.logger.exception("Error reloading cogs: %s", e)
            await ctx.respond("Error reloading cogs!", ephemeral=True)


def setup(bot: MasaBot) -> None:
    """Load the Admin cog into the bot.

    Args:
        bot: The bot instance this cog is attached to.

    Returns:
        None
    """

    bot.add_cog(Admin(bot))
