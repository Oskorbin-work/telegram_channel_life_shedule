from datetime import (datetime,
                      timedelta)
from telethon import TelegramClient
from telethon.tl.functions.messages import (GetHistoryRequest)
import pytz
from config_data import api_id,api_hash,channel_username,username, start_date, end_date

def get_current_UTC():
    kiev_timezone = pytz.timezone('Europe/Kyiv')
    current_utc = datetime.now(kiev_timezone).hour - datetime.now(pytz.utc).hour
    current_utc = timedelta(hours=current_utc)
    return current_utc

# Создаем клиент
client = TelegramClient(username, api_id, api_hash)


async def main(start_datetime, end_datetime):
    # ------------
    await client.start()
    result = await client(GetHistoryRequest(
        peer=channel_username,
        offset_date=start_datetime,  # Начальная дата поиска
        offset_id=0,
        add_offset=0,
        limit=10,  # Количество сообщений за запрос
        max_id=0,
        min_id=0,
        hash=0,
    ))
    await client.disconnect()
    #------------

    for message in result.messages:
        message_date = message.date+get_current_UTC()
        print(f"{message_date} : {message.message}")


date_format = '%Y.%m.%d'
start_datetime = datetime.strptime(start_date, date_format)
end_datetime = datetime.strptime(end_date, date_format)

with client:

    client.loop.run_until_complete(main(start_datetime,end_datetime))


