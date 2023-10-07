import asyncio
import datetime
import os
import time

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv
load_dotenv()

class MessageExistsException(Exception): pass
    
def tg_msgs_create_if_not_exists(td_id: int, td_date: datetime.date, tg_chat: str, tg_chat_id: int, tg_msg: str):
    _dir = os.path.join(os.environ['FILES_DIR'], tg_chat)
    os.makedirs(_dir, exist_ok=True)

    clean_date = str(td_date).replace(':', '_')
    clean_date = clean_date.replace('+', '_')
    clean_date = clean_date.replace(' ', '__')
    f_path = os.path.join(_dir, f'message_{td_id}_{clean_date}.txt')
    if not os.path.exists(f_path):
        open(f_path, 'wb').write(tg_msg.encode('utf-8'))

async def pull_messages(shutdown_path):
    all = 20 # How many messages to pull backwards
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
                        #tg_add_media_to_msg(msg_id, os.path.abspath(file_name))

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
