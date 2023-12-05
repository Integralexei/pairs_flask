
import requests
import json
import time

from dotenv import load_dotenv
import os

# Загрузка переменных окружения из .env
load_dotenv()

api_key = os.getenv('API_KEY_EXANTE_DEMO')
token = os.getenv('TOKEN_EXANTE_DEMO')

symbolId = 'SPY.ARCA'
duration_in_sec = 86400
api_version = "3.0"  # или "2.0"
# url = f"https://api.exante.eu/md/{api_version}/types" 
url = f"https://api-demo.exante.eu/md/{api_version}/ohlc/{symbolId}/{duration_in_sec}" 
params = {
    'size': '5000' # похоже что 5000 это лимит
}
# response = requests.get(url, params=params, auth=(api_key,token))

for i in range(10):
    response = requests.get(url, params=params, auth=(api_key,token))
    if response.status_code == 200:
        instruments = response.json()
        print(len(instruments))

        with open('h_data.json', 'w') as f:
            json.dump(instruments, f, indent=4)
        break
    elif response.status_code == 429:
            # Если получили ошибку 429, делаем паузу
            print("Превышен лимит запросов, ожидаем...")
            time.sleep(36)
    else:
        print("Ошибка при запросе:", response.status_code)
        

import datetime

# Ваша временная метка в миллисекундах
timestamp_ms = 1586412000000

# Преобразование в секунды
timestamp_s = timestamp_ms / 1000

# Преобразование в дату и время
date_time = datetime.datetime.fromtimestamp(timestamp_s)

print(date_time)