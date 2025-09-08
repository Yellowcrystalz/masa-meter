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

"""Configure Discord bot's enviroment.

Handle runtime mode selection and configures the Discord bot's token and guild
scope. In development mode, test bot token is used and development server is
scoped. In production mode, the actual bot token is used and production server
is scoped.
"""

import argparse
from enum import Enum

from config import (
    DISCORD_BOT_TOKEN, TEST_BOT_TOKEN, MAIN_GUILD_ID, DEV_GUILD_ID
)


class Mode(Enum):
    """Enumeration for bot runtime modes."""

    DEV = "development"
    PROD = "production"


parser: argparse.ArgumentParser = argparse.ArgumentParser()
parser.add_argument(
    "-p",
    "--prod",
    "--production",
    action="store_true",
    help="Run in production mode"
)
args: argparse.Namespace = parser.parse_args()

MODE: Mode = Mode.PROD if args.prod else Mode.DEV
BOT_TOKEN: str = DISCORD_BOT_TOKEN if MODE == Mode.PROD else TEST_BOT_TOKEN
GUILD_ID_LIST: list[int] = (
    [DEV_GUILD_ID, MAIN_GUILD_ID] if MODE == Mode.PROD else [DEV_GUILD_ID]
)
