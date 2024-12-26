"""
Как хранятся данные:
1.	Если точка, то вывести предупреждение. Возможна ошибка.
2.	Если внутри указано время, то точку искать не надо.+
3.  Дела вместят в себе время выполнения и перерыв.
4.  Сообщения может вмещать в себя не одно дело. А даже точку. +
5. Точка может свое время выполнения.
6. Дела могут повторяться и их надо суммировать
7. Дело могут быть внутри другого дела.
"""
import json
import re
list_tasks = ["Сон","Гигиена утро","Тренировка","Мытье","Дела категории Б",
              "Прием пищи","Дела","Перерывы","Техническое время","Гигиена вечер","ЧС","Остаток"]

dict_error = {}

address_file = 'app/modules/data_handler/data.json'

def data_to_json(data,date):
    """
    output all data to json.
    :param data: data all days
    :return:
    """
    with open(f'app/modules/google_sheets/data/{date}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f,indent=4, ensure_ascii=False)

def error_notification(date, error):
    """
    save an error message

    :param date: data
    :param error: error message
    :return: save an error message
    """
    dict_error[date] = error


def calculate_time_difference_in_decimal(start_hours,start_minutes,end_hours, end_minutes):
    """
    24-format time to decimal and get different
    :param start_hours: start hour
    :param start_minutes: start minutes
    :param end_hours: end hours
    :param end_minutes:  end minutes
    :return:
    get different times
    """
    # str to int
    start_hours, start_minutes, end_hours, end_minutes = int(start_hours), int(start_minutes), int(end_hours), int(end_minutes)

    # Conversion to minutes for easier calculations
    start_time_in_minutes = start_hours * 60 + start_minutes
    end_time_in_minutes = end_hours * 60 + end_minutes

    # Calculating the difference in minutes
    difference_in_minutes = end_time_in_minutes - start_time_in_minutes

    # Converting a difference to decimal
    decimal_difference = difference_in_minutes / 60
    return decimal_difference

def calculate_time_in_decimal(hours,minutes):
    """
    24-format time to decimal
    :param hours: hours
    :param minutes: minutes
    :return:
    get time in format decimal
    """
    hours,minutes = int(hours), int(minutes)
    # Conversion to minutes for easier calculations
    time_in_minutes = hours * 60 + minutes

    # Converting a difference to decimal
    decimal_difference = time_in_minutes / 60
    return decimal_difference

# Разбивка данных по правильным сообщениям.
def slit_tasks(data):
    """
    Message can have a few events. I have split it.
    :param data: It is a message
    :return:
        add a new events
    """
    dict_tasks = {}
    for date, events in data.items():
        dict_tasks[date] = []
        for event in events:
            if "\n" in event["text"]:
                list_add_tasks = [line for line in event["text"].split("\n") if line.strip()]
                for task in list_add_tasks:
                    dict_tasks[date].append({"time": event["time"],"text": task})
            else:
                dict_tasks[date].append(event)
    return dict_tasks

def structure_tasks(date):
    """
    handler data one day to format for google sheet:

    :param date: date day
    :return:
    dict tasks one day.
    """
    dict_tasks = {}
    dict_tasks[date] = []
    def search_task(events, date, number):
        """
        check tasks/events
        :param events: all tasks
        :param date: one date
        :param number: Index variable
        :return:
        dict tasks one day.
        """
        # check an exit events.
        if len(events) != number:
            event = events[number]
        else:
            return dict_tasks
        # check next step in the events
        if len(events) != number + 1:
            next_event = events[number + 1]
        else:
            next_event = ""

        # Searches for an error if such a case does have wrong words
        if not any(task in event["text"] for task in list_tasks) and "." not in event["text"]:
            error_notification(str(date),"Событие " + event["text"] + " не содержит правильное дело")
            return dict_tasks
        else:
            # work to tasks
            for task in list_tasks:
                # The task is identical with keywords.
                if task == event["text"]:
                    # task have dot in text
                    if "." in next_event["text"]:
                        time = calculate_time_difference_in_decimal(event["time"][0:2], event["time"][3:5],
                                                                    next_event["time"][0:2], next_event["time"][3:5])
                        dict_tasks[date].append({"task": task, "time": time})
                        # task name "Дела" and it's not have dot.
                        if "." != next_event["text"] and task == "Дела":
                            time_tasks_and_break = [item.strip() for item in re.split(r"[,:]", next_event["text"][1:])]
                            # add task Перерывы
                            dict_tasks[date].append({"task": "Перерывы",
                                                     "time": calculate_time_in_decimal(time_tasks_and_break[2],
                                                                                       time_tasks_and_break[3])})
                        return search_task(events, date, number + 2)
                    break
                # if task have keywords and something too
                elif task in event["text"]:
                    parts_time = event["text"][len(task):].lstrip()
                    parts_time = re.split(r"[-:]", parts_time)
                    time = calculate_time_difference_in_decimal(parts_time[0], parts_time[1], parts_time[2],
                                                                parts_time[3])
                    dict_tasks[date].append({"task": task, "time": time})
                    return search_task(events, date, number + 1)
        # print an error message if a task contains wrong words, etc
        error_notification(date, event["text"] + " Не имеет условий для решения")
        return dict_tasks

    return search_task


def get_days():
    """
    get all days from JSON
    :return:
    """
    with open(address_file, 'r') as f:
        data = json.load(f)
    return data


def handler():
    """
    handler all data for all days
    :return:
    outputs processed data as JSON
    """
    data = get_days()

    if data:
        dict_tasks = slit_tasks(data)
        for date, events in dict_tasks.items():
            recursive_func = structure_tasks(date)
            data_one_day = recursive_func(events, date, 0)
            """for date, tasks in data.items():
                for task in tasks:
                    print(f"  - Задача: {task['task']}, Время: {task['time']} часов")"""
            data_to_json(data_one_day[date],date)

        for date, tasks in dict_error.items():
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(f"Дата: {date}, Ошибка: {tasks}")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    else:
        print("Данных нету")

if __name__ == "__main__":
    handler()