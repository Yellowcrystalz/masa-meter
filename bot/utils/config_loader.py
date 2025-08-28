"""
Config Token Loader

This utility loads the correct token from the config file depending on the enviroment. Argument
flags control which mode the bot is in. If the '-p', '--prod','production' flags is passed when
starting the bot, the production token is used, otherwise the testing token is defaulted to.
"""

import argparse
from config import DISCORD_TOKEN, TEST_TOKEN


def get_token() -> str:
    """
    Retreives a Discord API based on command line argument flags.

    -- If run with '-p', '--prod', '--production', the production token is returned
    -- Othewise, the test token is returned.

    Returns:
        str: A Discord API token. Either the test or production token.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--prod", "--production", action="store_true", help="Run in production mode")
    args = parser.parse_args()

    if args.prod:
        token = DISCORD_TOKEN
    else:
        token = TEST_TOKEN

    return token
