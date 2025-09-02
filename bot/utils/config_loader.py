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

"""Load the correct Discord API token from the config file.

Determine whether to run in production or testing mode based on command-line
flags. If '-p', '--prod', or '--production' is passed when starting the bot,
use the production token; otherwise, use the test token.
"""

import argparse
from config import DISCORD_BOT_TOKEN, TEST_BOT_TOKEN


def get_token() -> str:
    """Retreive a Discord API based on command-line argument flags.

    Parse the command-line arguments to determine whether to run the bot
    in production or testing mode. Return the corresponding Discord token.

    Returns:
        A Discord API token. Either the test or production token.
    """

    parser: argparse.ArgumentParser = argparse.ArgumentParser()

    parser.add_argument(
        "-p",
        "--prod",
        "--production",
        action="store_true",
        help="Run in production mode"
    )

    args: argparse.Namespace = parser.parse_args()

    if args.prod:
        token: str = DISCORD_BOT_TOKEN
    else:
        token: str = TEST_BOT_TOKEN

    return token
