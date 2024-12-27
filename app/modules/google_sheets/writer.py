from modules.google_sheets.sheets_api import api
from modules.google_sheets.google_workcloud.confid_data import (
  SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME)

def get_data(service):
	sheet = service.spreadsheets()
	result = (
		sheet.values()
		.get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
		.execute()
	)
	values = result.get("values", [])

	if not values:
		print("No data found.")
		return

	for row in values:
		print(row)



def writer():
	service = api()
	if service != "error":
		get_data(api())


if __name__ == "__main__":
	writer()
