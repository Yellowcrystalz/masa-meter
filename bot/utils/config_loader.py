import argparse
from config import DISCORD_TOKEN, TEST_TOKEN


def get_token():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--prod", "--production", action="store_true", help="Run in production mode")
    args = parser.parse_args()

    if args.prod:
        token = DISCORD_TOKEN
    else:
        token = TEST_TOKEN

    return token
