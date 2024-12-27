from modules.google_sheets.sheets_api import api
from modules.google_sheets.google_workcloud.config_data import (
  SAMPLE_SPREADSHEET_ID, GET_RANGE_NAME)

from datetime import datetime
import os
import json

directory_json = "app/modules/google_sheets/data"

def get_row_data(directory,date):
	row_tasks = {
		"Сон":0.0,
		"Гигиена утро": 0.0,
		"Тренировка":0.0,
		"Мытье": 0.0,
		"Дела категории Б":0.0,
		"Прием пищи": 0.0,
		"Гигиена вечер":0.0,
		"ЧС":0.0,
		"Перерывы": 0.0,
		"Техническое время": 0.0,
		"Дела":0.0
	}
	date = datetime.strptime(date,"%m/%d/%Y")
	date = date.strftime("%Y-%m-%d")
	address_file = directory+"/"+date+".json"
	with open(address_file, 'r') as f:
		try:
			tasks = json.load(f)
			tasks = tasks[date]
		except FileNotFoundError:
			print("Указанный файл не найден по заданному пути")
			return
		except IsADirectoryError:
			print("Указанный путь ведет к директории, а не к файлу.")
			return
		except PermissionError:
			print("Возникает, если проблемы с правами доступа")
			return
		except json.JSONDecodeError:
			print("Содержимое файла не является корректным JSON.")
			return

	for task in tasks:
		row_tasks[task["task"]]= task['time']+ row_tasks[task["task"]]

	for key, value in row_tasks.items():
		if value == 0.0:
			if key not in ["ЧС","Перерывы","Гигиена утро", "Тренировка","Гигиена вечер"]:
				row_tasks[key] = ""
	return row_tasks


# AB это колонка ПОЛЕЗНЫЕ ДЕЛА
def add_data_row(date, number_row,sheet,different_time):
	try:
		row_data = get_row_data(directory_json,date)
	except:
		print("Данные дня " + date + " не корректные")
	range_put = f'JOURNAL!V{number_row}:AF{number_row}'  # Діапазон, куди вставлятимемо дані
	values = [
		[
			row_data['Сон'],
			row_data['Гигиена утро'],
			row_data['Тренировка'],
			row_data['Мытье'],
			row_data['Дела категории Б'],
			row_data['Прием пищи'],
			row_data['Гигиена вечер'],
			row_data['ЧС'],
			row_data['Перерывы'],
			row_data['Дела']-row_data['Перерывы']-float(different_time)
		],
	]
	body = {'values': values}
	sheet.values().update(
		spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_put,
		valueInputOption='USER_ENTERED', body=body).execute()



def row_index(values, name,sheet):
	"""Возвращает индекс первого элемента в списке, начинающегося со строки name.

	Args:
	values: Список списков.
	name: Строка для поиска в качестве первого элемента вложенных списков.
	Returns:
	Индекс первого найденного элемента или None, если элемент не найден.
	"""
	for index, value in enumerate(values):
		if value[0] == str(name):
			# value[31] это колонка ПОЛЕЗНЫЕ ДЕЛА
			try:
				value[31]
			except NameError:
				print(f"Ячейка Полезные дела пустая!\nДата такая:{name}")
			add_data_row(name,index+1,sheet,value[31])
			break

def find_json_files(directory):
	"""
	  Функция для поиска всех JSON файлов в указанной директории.

	  Args:
	    directory: Путь к директории для поиска.

	  Returns:
	    Список имен найденных JSON файлов.
	  """
	json_files = []
	for root, dirs, files in os.walk(directory):
		for file in files:
			if file.endswith(".json"):
				json_files.append(os.path.join(root, file))
		return json_files

def sheet_data(service,json_files):
	sheet = service.spreadsheets()
	result = (
		sheet.values()
		.get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=GET_RANGE_NAME)
		.execute()
	)
	values = result.get("values", [])

	if not values:
		print("No data found.")
		return

	for path in json_files:
		name = os.path.splitext(os.path.basename(path))[0]
		name = datetime.strptime(name, "%Y-%m-%d")
		name = name.strftime("%m/%d/%Y")
		row_index(values, name,sheet)

def writer():
	json_files = find_json_files(directory_json)
	if not json_files:
		print("JSON файлы не найдены.")
		return
	service = api()
	if service != "error":
		sheet_data(api(),json_files)
	else:
		print("API не работает")
		return

if __name__ == "__main__":
	writer()

