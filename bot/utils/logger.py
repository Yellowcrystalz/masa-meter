"""
Logging Configuration

This utility sets up logging for the Discord bot. It creates two separate loggers for bot events
(app_logger) and the Discord's own internal logger (discord_logger).

- app_logger: Logs bot specific events. Specified by the developer.
- discord_logger: Logs discord.py internal events.
"""

import logging

from config import APP_LOG_PATH, DISCORD_LOG_PATH


formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s %(name)s: %(message)s]",
    datefmt="%Y-%m-%d %H:%M:%s"
)

# -
# Bot Application Logger
# -
app_handler = logging.FileHandler(APP_LOG_PATH, encoding="utf-8", mode="a")
app_handler.setFormatter(formatter)

app_logger = logging.getLogger("bot")
app_logger.setLevel(logging.INFO)
app_logger.addHandler(app_handler)
app_logger.propagate = False                    # Prevents double logging to root

# -
# Discord Bot Logger
# -
discord_handler = logging.FileHandler(DISCORD_LOG_PATH, encoding="utf-8", mode="a")
discord_handler.setFormatter(formatter)

discord_logger = logging.getLogger("discord")
discord_logger.setLevel(logging.INFO)
discord_logger.addHandler(discord_handler)
discord_logger.propagate = False                # Prevents double logging to root
