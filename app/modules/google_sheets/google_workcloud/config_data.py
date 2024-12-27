import configparser

config = configparser.ConfigParser()
config.read('app/modules/google_sheets/google_workcloud/.config')

#google sheet
SAMPLE_SPREADSHEET_ID = config['google']['SAMPLE_SPREADSHEET_ID']
GET_RANGE_NAME = config['google']['SHEET_NAME']+ config['google']['GET_RANGE_NAME']
PATH_TO_TOKEN = config['google']['PATH_TO_TOKEN']
CLIENT = config['google']['CLIENT']
SCOPES = [config['google']['SCOPES']]