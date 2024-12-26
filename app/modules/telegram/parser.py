from datetime import (datetime,
                      timedelta)
from telethon import TelegramClient
from telethon.tl.functions.messages import (GetHistoryRequest)
import pytz
from modules.telegram.config_data import api_id,api_hash,channel_username,username, start_date
import json

def normalize_text(text):
    """
    change letters
    :param text: any text
    :return:
    normal text
    """
    text = text.replace('ё', 'е')  # Замена "ё" на "е"
    text = text.replace('Ë', 'Е')  # Замена "Ë" на "Е"
    return text

def get_current_UTC():
    """
    get UTC Ukraine
    :return:
    UTC Ukraine
    """
    kiev_timezone = pytz.timezone('Europe/Kyiv')
    current_utc = datetime.now(kiev_timezone).hour - datetime.now(pytz.utc).hour
    current_utc = timedelta(hours=current_utc)
    return current_utc

def format_date(date):
    """
    return correct time format:
     incorrect: 2:2
     correct: 02:02
    :param date:
    :return:
    correct format-date
    """
    return f"{date.hour:02d}:{date.minute:02d}"

def check_start_date(messages,end_date):
    """
    get all data from one day
    :param messages:
    :param end_date:
    :return:
    """
    temp_list = list()
    for message in messages:
        if end_date.date() ==message.date.date():
            date_day = format_date(message.date + get_current_UTC())
            temp_list.append({"time":date_day, "text":message.message})
        elif end_date.date() >message.date.date():
            return temp_list[::-1]
    return temp_list[::-1]

def data_to_json(data):
    """
    output data to json.
    :param data: data all day
    """
    with open('app/modules/data_handler/data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f,indent=4, ensure_ascii=False)

# create a client
client = TelegramClient(username, api_id, api_hash)

# dict to all messages
final = {}

async def parser(start_datetime):
    """
    parser
    :param start_datetime: start date to search data
    """
    days = datetime.now()-start_datetime
    for i in range(days.days):
        end_data = datetime.now() - timedelta(days=i)
        # ------------
        await client.start()
        result = await client(GetHistoryRequest(
            peer=channel_username,
            offset_date=end_data,  # end date search
            offset_id=0,
            add_offset=0,
            limit=50, 
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


