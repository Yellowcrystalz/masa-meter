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

""" Configure logging for the Discord bot

Set up two separate loggers: one for application-specific bot events and
one for Discord's internal events. Log messages are written to files with
a timestamped format.

Attributes:
    app_logger: Logs the applications events.
    discord_logger: Logs discord internal events and errors.
"""

import logging

from config import APP_LOG_PATH, DISCORD_LOG_PATH


formatter: logging.Formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s %(name)s: %(message)s]",
    datefmt="%Y-%m-%d %H:%M:%s"
)

# -----------------------------------------------------------------------
# Bot Application Logger
# -----------------------------------------------------------------------
app_handler: logging.FileHandler = logging.FileHandler(
    APP_LOG_PATH, encoding="utf-8", mode="a"
)
app_handler.setFormatter(formatter)

app_logger: logging.Logger = logging.getLogger("bot")
app_logger.setLevel(logging.INFO)
app_logger.addHandler(app_handler)
app_logger.propagate = False                # Prevents double logging to root

# -----------------------------------------------------------------------
# Discord Bot Logger
# -----------------------------------------------------------------------
discord_handler: logging.FileHandler = logging.FileHandler(
    DISCORD_LOG_PATH, encoding="utf-8", mode="a"
)
discord_handler.setFormatter(formatter)

discord_logger: logging.Logger = logging.getLogger("discord")
discord_logger.setLevel(logging.INFO)
discord_logger.addHandler(discord_handler)
discord_logger.propagate = False            # Prevents double logging to root
