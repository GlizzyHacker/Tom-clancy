import logging.handlers
import os
import requests
from dotenv import load_dotenv

load_dotenv()

LOG_WEBHOOK_URL = os.getenv("LOG_WEBHOOK_URL")
COLORS = {"DEBUG":16777215,"INFO":65280,"WARNING":16744192,"ERROR":16711680,"CRITICAL":9109504} # Színek decimal value

class DiscordHandler(logging.Handler):
    def emit(self, record):
        log = self.format(record)
        embed = {
            "title": record.levelname,
            "description": log,
            "color": COLORS[record.levelname]
        }
        payload = {"embeds": [embed]}
        requests.post(LOG_WEBHOOK_URL, json=payload)

def setup_handler():
    logger = logging.getLogger("discord")

    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", date_format)

    handler = DiscordHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)