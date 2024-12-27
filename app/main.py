from modules.telegram.parser import start_parser
from modules.data_handler.handler import handler
from modules.google_sheets.writer import writer
import os


def delete_old_json_files():
    path_to_folder = "app/modules/google_sheets/data"
    for file in os.listdir(path_to_folder):
        if file.endswith(".json"):
            path_to_file = os.path.join(path_to_folder, file)
            os.remove(path_to_file)

if __name__ == "__main__":
    try:
        delete_old_json_files()
    except:
        print("Не смог удалить json с прошлого запроса")
    else:
        print("Удаление старых json – ок")
    # get data from a telegram channel
    try:
        start_parser()
    except:
        print("Поломка в парсере")
    else:
        print("Парсер – ок")
    # handler data
    try:
        handler()
    except:
        print("Поломка в Обработчике")
    else:
        print("Обработчик – ок")

    try:
        # Добавь тут удаление файлов из app/modules/google_sheets/data
        writer()
    except:
        print("Отправить данные в гугл таблицу не получилось...")
    else:
        print("Загрузка данных в гугл таблицу - ок")
        print("Работа завершена!")




