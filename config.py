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
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

BOT_DIR = BASE_DIR / "bot"
COGS_DIR = BOT_DIR / "cogs"

APP_LOG_PATH = DATA_DIR / "application.log"
DISCORD_LOG_PATH = DATA_DIR / "discord.log"

# Frontend
FRONTEND_DIR = BASE_DIR / "frontend"
HTML_DIR = FRONTEND_DIR / "html"

INDEX_PATH = FRONTEND_DIR / "index.html"
