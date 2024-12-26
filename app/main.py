from modules.telegram.parser import start_parser
from modules.data_handler.handler import handler



if __name__ == "__main__":
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




