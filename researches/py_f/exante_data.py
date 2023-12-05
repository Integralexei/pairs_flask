
import requests
import json

from dotenv import load_dotenv
import os

# Загрузка переменных окружения из .env
load_dotenv()

api_key = os.getenv('API_KEY_EXANTE_DEMO')
token = os.getenv('TOKEN_EXANTE_DEMO')

api_version = "3.0"  # или "2.0"
# url = f"https://api.exante.eu/md/{api_version}/types" 
url = f"https://api-demo.exante.eu/md/{api_version}/types/STOCK" 

response = requests.get(url, auth=(api_key,token))

if response.status_code == 200:
    print('222')
    instruments = response.json()
    # print(json.dumps(instruments, indent=4))
    print('!')
    print(len(instruments))

    # print('1111')
    # with open('data.json', 'w') as f:
    #     json.dump(instruments, f, indent=4)
else:
    print("Ошибка при запросе:", response.status_code)
