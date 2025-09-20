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

"""Configure directory paths, file paths, and enviroment variables.

This module provides constants for general paths, database locations,
Discord bot configuration, logging, and frontend assets. Environment
variables are loaded from a `.env` file in the base directory.
"""

import os
from pathlib import Path

from dotenv import load_dotenv


# General
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

load_dotenv(BASE_DIR / ".env")

# Database
DATABASE_PATH = DATA_DIR / "masa_meter.db"

# Discord Bot
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
TEST_BOT_TOKEN = os.getenv("TEST_BOT_TOKEN")        # For testing purposes
MAIN_GUILD_ID = int(os.getenv("MAIN_GUILD_ID"))
DEV_GUILD_ID = int(os.getenv("DEV_GUILD_ID"))

BOT_DIR = BASE_DIR / "bot"
COGS_DIR = BOT_DIR / "cogs"
ASSETS_DIR = BOT_DIR / "assets"
AUDIO_DIR = ASSETS_DIR / "audio"

APP_LOG_PATH = DATA_DIR / "application.log"
DISCORD_LOG_PATH = DATA_DIR / "discord.log"

JOIN_MP3_PATH = AUDIO_DIR / "join.mp3"
LEAVE_MP3_PATH = AUDIO_DIR / "leave.mp3"