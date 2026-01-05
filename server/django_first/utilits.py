from datetime import datetime
import requests
import uuid

def create_time():
    now = datetime.now()
    return now.strftime("%d-%m-%Y %H:%M:%S")

def get_tocken():
    """Получает и возвращает актуальный access_token для GigaChat API."""
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    
    # scope определяет права доступа (для физ. лиц - GIGACHAT_API_PERS)
    payload = {'scope': 'GIGACHAT_API_PERS'}
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': str(uuid.uuid4()),  # ГЕНЕРИРУЕМ УНИКАЛЬНЫЙ ID
        'Authorization': 'Bearer MDE5YjMzMzUtODVmNy03NmY5LTgxNGUtNjU5M2ZjMzcyMTg2OjA5NWM5NTdiLTQ4YjQtNDU3Yy04ZWQ5LTUzNjA5Yzk0ZWY0ZQ=='  # ДОБАВЛЯЕМ "Bearer"
    }
    
    # Временное отключение проверки SSL для разработки (verify=False)
    response = requests.post(url=url, headers=headers, data=payload, verify=False)
    
    # Парсим JSON и извлекаем токен
    response_data = response.json()
    access_token = response_data['access_token']
    return access_token
