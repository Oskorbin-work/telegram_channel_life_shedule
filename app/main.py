from datetime import datetime, timedelta
from telethon import TelegramClient
from telethon.tl.functions.messages import (GetHistoryRequest)

import pytz

import configparser


config = configparser.ConfigParser()
config.read('app/.config')

# Get credentials from the .config file
api_id = config['settings']['TELEGRAM_API_ID']
api_hash = config['settings']['TELEGRAM_API_HASH']
channel_username = config['settings']['CHANNEL_NAME']
username = config['settings']['USERNAME']
phone = config['settings']['PHONE_NUM']


# Создаем клиент
client = TelegramClient('oskorbin', api_id, api_hash)

async def main():
    await client.start()
    result = await client(GetHistoryRequest(
        peer=channel_username,
        offset_date=datetime.now(),
        offset_id = 0,
        add_offset=0,
        limit=10,
        max_id=0,
        min_id=0,
        hash=0,
    ))
    # Потом перевести в отдельную функцию
    #-------------------------------------
    kiev_timezone = pytz.timezone('Europe/Kyiv')
    current_utc = datetime.now(kiev_timezone).hour - datetime.now(pytz.utc).hour
    two_hours = timedelta(hours=current_utc)
    # -------------------------------------
    for message in result.messages:
        message_date = message.date+two_hours
        print(f"{message_date} : {message.message}")
    await client.disconnect()


with client:
    client.loop.run_until_complete(main())
