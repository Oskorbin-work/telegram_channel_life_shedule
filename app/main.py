from modules.telegram.parser import start_parser
from modules.data_handler.handler import handler
from modules.google_sheets.writer import writer
import os

def print_color(text, color):
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m'
    }
    print(colors[color] + text + colors['reset'])

def delete_old_json_files():
    path_to_folder = "app/modules/google_sheets/data"
    for file in os.listdir(path_to_folder):
        if file.endswith(".json"):
            path_to_file = os.path.join(path_to_folder, file)
            os.remove(path_to_file)

if __name__ == "__main__":
    print_color("Удаляем старые данные с прошлых разов...","cyan")
    # delete old json-files with dates...
    try:
        delete_old_json_files()
    except:
        print_color("Не смог удалить json с прошлого запроса","red")
    else:
        print_color("       Удаление старых json – ок","green")
    print_color("Берем данные из telegram...","cyan")
    # get data from a telegram channel
    try:
        start_parser()
    except:
        print_color("Поломка в парсере","red")
    else:
        print_color("       Парсер – ок","green")
    print_color("Приводим данные к состоянию формата Google Sheets...","cyan")
    # handler data
    try:
        handler()
    except:
        print_color("       Поломка в Обработчике","red")
    else:
        print_color("       Обработчик – ок","green")
    print_color("Отправка данных в Google Sheets...","cyan")
    try:
        writer()
    except:
        print_color("Отправить данные в гугл таблицу не получилось...","red")
    else:
        print_color("       Загрузка данных в гугл таблицу - ок","green")
        print_color("Работа завершена!","magenta")




