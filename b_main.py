#!/usr/bin/env python3

import sys
import os

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv
load_dotenv()

SAVE_TO_DIR = 'message_archive'

client = TelegramClient(StringSession(open(os.environ['TG_SESSION_STRING_PATH'], 'r').read()), os.environ['TG_API_ID'], os.environ['TG_API_HASH'])

async def save_message(message, channel_name):
    if message.text:
        channel_directory = os.path.join(SAVE_TO_DIR, channel_name)
        os.makedirs(channel_directory, exist_ok=True)

        message_file = os.path.join(channel_directory, f'message_{message.id}_.txt')
        print(f"saving message {message.id} to {message_file}")
        with open(message_file, 'w', encoding='utf-8') as file:
            file.write(message.text)

async def main(channel_name):
    await client.start()

    while True:
        channel_entity = await client.get_entity(channel_name)

        async for message in client.iter_messages(channel_entity, limit=None):
            await save_message(message, channel_name)

if __name__ == '__main__':
    assert len(sys.argv) == 2, f"usage: {sys.argv[0]} <channel name>"

    channel_name = sys.argv[1]
    print(f"Saving messages from channel {channel_name}")
    with client:
        client.loop.run_until_complete(main(channel_name))