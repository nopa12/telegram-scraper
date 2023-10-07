SAVE_TO_DIR = 'message_archive'

CHANNELS = [
    "hamas",
    "palestine_aqsaa",
    "PalpostN",
    "gazaalannet"
]

import asyncio
import datetime
import os
import time

import sqlalchemy

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv
load_dotenv()

import db

class MessageExistsException(Exception): pass

def tg_add_media_to_msg(msg_id, tg_file_path: str):
    with db.transaction_context() as conn:
        msg = conn.query(db.TgMsgsRaw).filter_by(id=msg_id).first()
        if not msg:
            print(f"message not found for {msg}")
            return
        
        print(f"adding media for message {msg.id}")
        db_tg_media = db.TgMedia(tg_msg_id=msg.id, tg_file_path=tg_file_path)
        conn.add(db_tg_media)
        conn.flush()
    
def tg_msgs_create_if_not_exists(td_id: int, td_date: datetime.date, tg_chat: str, tg_chat_id: int, tg_msg: str):
    with db.transaction_context() as conn:
        existing_msg = conn.query(db.TgMsgsRaw).filter_by(tg_id=td_id, tg_chat_id=tg_chat_id).first()
        if existing_msg:
            print(f"message {tg_chat_id} {td_id} exists")
            raise MessageExistsException()
        
        print(f"adding message {td_id}")
        db_tg_msg = db.TgMsgsRaw(tg_id=td_id, tg_date=td_date, tg_chat=tg_chat, tg_chat_id=tg_chat_id, tg_msg=tg_msg)
        conn.add(db_tg_msg)
        conn.flush()
        return db_tg_msg.id

async def pull_messages(shutdown_path):
    all = 15
    task1 = pull_tg_channel_msgs_async("hamas", all, shutdown_path)
    task2 = pull_tg_channel_msgs_async("palestine_aqsaa", all, shutdown_path)
    task3 = pull_tg_channel_msgs_async("PalpostN", all, shutdown_path)
    task4 = pull_tg_channel_msgs_async("gazaalannet", all, shutdown_path)
    t = await asyncio.gather(task1, task2, task3, task4)

async def pull_tg_channel_msgs_async(channel_username, limit, shutdown_path):
    if os.path.exists(shutdown_path):
        print("Shutting down...")
        return

    tg_session_string = open(os.environ['TG_SESSION_STRING_PATH'], 'r').read()
    client = TelegramClient(StringSession(tg_session_string), os.environ['TG_API_ID'], os.environ['TG_API_HASH'])
    try:
        await client.start()
        print("Connected to Telegram")

        channel_entity = await client.get_entity(channel_username)
        print("Getting messages")
        messages = await client.get_messages(channel_entity, limit=limit)

        print("iterating messages")
        for message in messages:
            r = False
            while not r:
                try:
                    msg_id = tg_msgs_create_if_not_exists(message.id, message.date, channel_username, message.chat_id, message.text)
                    if message.media:
                        #for i, media in enumerate(message.media, start=1):
                        if hasattr(message.media, 'photo'):
                            file_extension = 'jpg'
                        elif hasattr(message.media, 'document'):
                            file_extension = 'mp4'
                        else:
                            break

                        file_name = os.path.join(os.environ['FILES_DIR'], channel_username, f'media_{message.id}.{file_extension}')
                        print(f"downloading {file_name} ...")
                        await client.download_media(message.media, file_name)
                        print(f"downloaded {file_name}")
                        tg_add_media_to_msg(msg_id, os.path.abspath(file_name))

                    r = True
                except MessageExistsException:
                    r = True
                # except sqlalchemy.exc.OperationalError:
                #     r = None
            if os.path.exists(shutdown_path):
                print("Shutting down...")
                break

    finally:
        await client.disconnect()

if __name__ == '__main__':
    while not os.path.exists(os.environ['SHUTDOWN_PATH']):
        asyncio.run(pull_messages(os.environ['SHUTDOWN_PATH']))
        time.sleep(0.1)
