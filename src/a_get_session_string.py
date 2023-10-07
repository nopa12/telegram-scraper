#!/usr/bin/env python3
import os

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv
load_dotenv()

with TelegramClient(StringSession(), os.environ['TG_API_ID'], os.environ['TG_API_HASH']).start(phone=os.environ['TG_PHONE_NUMBER']) as client:
    open(os.environ['TG_SESSION_STRING_PATH'], 'w').write(client.session.save())