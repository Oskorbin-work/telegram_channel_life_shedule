import configparser


config = configparser.ConfigParser()
config.read('app/modules/telegram/.config')

# Get credentials from the .config file
api_id = config['telegram']['TELEGRAM_API_ID']
api_hash = config['telegram']['TELEGRAM_API_HASH']
channel_username = config['telegram']['CHANNEL_NAME']
username = config['telegram']['USERNAME']
phone = config['telegram']['PHONE_NUM']

start_date = config['other']['START_DATE']
