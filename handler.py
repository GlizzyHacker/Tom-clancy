import logging.handlers
import os
import requests
from dotenv import load_dotenv

load_dotenv()

LOG_WEBHOOK_URL = os.getenv("LOG_WEBHOOK_URL")

class DiscordHandler(logging.Handler):
    def emit(self, record):
        log = self.format(record)
        requests.post(LOG_WEBHOOK_URL, json={"content": log})

def setup_handler():
    logger = logging.getLogger("discord")
    logger.setLevel(logging.ERROR)

    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", date_format)

    handler = DiscordHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)