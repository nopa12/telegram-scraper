#!/usr/bin/env python3

import asyncio
import sys
import os
import threading
import time

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv
load_dotenv()

SAVE_TO_DIR = 'message_archive'

CHANNELS = [
    "hamas",
    "palestine_aqsaa",
    "PalpostN",
    "gazaalannet"
]

async def save_message(client, message, channel_name):
    channel_directory = os.path.join(SAVE_TO_DIR, channel_name)
    os.makedirs(channel_directory, exist_ok=True)

    if message.text:
        message_file = os.path.join(channel_directory, f'message_text_{message.id}_{time.time()}.txt')
        if not os.path.isfile(message_file):
            print(f"{channel_name}: saving message {message.id}")
            with open(message_file, 'w', encoding='utf-8') as file:
                file.write(message.text)

    if message.photo:
        index = 0
        media_file = os.path.join(channel_directory, f'message_photo_{message.id}_{time.time()}_{index}.jpg')
        if not os.path.isfile(media_file):
            print(f"{channel_name}: saving photo {media_file} ...")
            await client.download_media(media_file, file=media_file)
            print(f"{channel_name}: saved photo {media_file}")
    
    if message.media:
        index = 0
        media_file = os.path.join(channel_directory, f'message_video_{message.id}_{time.time()}_{index}_.mp4')
        if not os.path.isfile(media_file):
            print(f"{channel_name}: saving video {media_file} ...")
            await client.download_media(message.media, file=media_file)
            print(f"{channel_name}: saved video {media_file}")

async def download_channel(client, channel_name):
    await client.start()
    print(f"{channel_name}: connected")

    channel_entity = await client.get_entity(channel_name)

    async for message in client.iter_messages(channel_entity, limit=None):
        await save_message(client, message, channel_name)

def thread_channel(channel_name):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    client = TelegramClient(StringSession(open(os.environ['TG_SESSION_STRING_PATH'], 'r').read()), os.environ['TG_API_ID'], os.environ['TG_API_HASH'])
    while True:
        print(f"{channel_name}: connecting...")
        with client:
            client.loop.run_until_complete(download_channel(client, channel_name))
        time.sleep(0.1)

if __name__ == '__main__':
    threads = []
    for i in range(len(CHANNELS)):
        thread = threading.Thread(target=thread_channel, args=(CHANNELS[i], ))
        threads.append(thread)
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()