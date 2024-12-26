from datetime import (datetime,
                      timedelta)
from telethon import TelegramClient
from telethon.tl.functions.messages import (GetHistoryRequest)
import pytz
from modules.telegram.config_data import api_id,api_hash,channel_username,username, start_date
import json

def normalize_text(text):
    text = text.replace('ё', 'е')  # Замена "ё" на "е"
    text = text.replace('Ë', 'Е')  # Замена "Ë" на "Е"
    return text

def get_current_UTC():
    kiev_timezone = pytz.timezone('Europe/Kyiv')
    current_utc = datetime.now(kiev_timezone).hour - datetime.now(pytz.utc).hour
    current_utc = timedelta(hours=current_utc)
    return current_utc


def format_date(date):
    return f"{date.hour:02d}:{date.minute:02d}"

def check_start_date(messages,end_date):
    temp_list = list()
    # format_date(message.date + get_current_UTC())
    for message in messages:
        if end_date.date() ==message.date.date():
            date_day = format_date(message.date + get_current_UTC())
            temp_list.append({"time":date_day, "text":message.message})
        elif end_date.date() >message.date.date():
            return temp_list[::-1]
    return temp_list[::-1]

def data_to_json(data):
    with open('app/modules/data_handler/data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f,indent=4, ensure_ascii=False)

# Создаем клиент
client = TelegramClient(username, api_id, api_hash)

final = {}
async def parser(start_datetime):
    days = datetime.now()-start_datetime
    for i in range(days.days):
        end_data = datetime.now() - timedelta(days=i)
        # ------------
        await client.start()
        result = await client(GetHistoryRequest(
            peer=channel_username,
            offset_date=end_data,  # Начальная дата поиска
            offset_id=0,
            add_offset=0,
            limit=50,  # Количество сообщений за запрос
            max_id=0,
            min_id=0,
            hash=0,
        ))
        await client.disconnect()
        current_data = end_data.date()- timedelta(days=1)
        result = check_start_date(result.messages, end_data - timedelta(days=1))

        if result:
            list_task = [{'time': task['time'], 'text': normalize_text(task['text'])} for task in result]
            final[str(current_data)] = list_task
    data_to_json(final)


date_format = '%Y.%m.%d'
start_datetime = datetime.strptime(start_date, date_format)

def start_parser():
    with client:

        client.loop.run_until_complete(parser(start_datetime))


