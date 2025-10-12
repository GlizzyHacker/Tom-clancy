#!/usr/local/lib/python3.7
import os
import sys
from threading import Timer
import time
import logging
import asyncio
from subprocess import Popen
from dotenv import load_dotenv
from log_handler import DiscordHandler;

load_dotenv()

FOREVER_WEBHOOK_URL = os.getenv("FOREVER_WEBHOOK_URL")

delay = 2
filename = sys.argv[1]

handler = DiscordHandler(FOREVER_WEBHOOK_URL)

while True:
    print("\nStarting " + filename)
    p = Popen("python " + filename, shell=True)
    p.wait()
    
    #process exited
    handler.emit(logging.LogRecord('forever', logging.CRITICAL, "/", "0", msg=f"Program \"{filename}\" stopped. Restarting in {delay} seconds.", args = None, exc_info= None))

    time.sleep(delay)

    #binary exponential backoff
    delay *= 2
    delay = min(600,delay)
