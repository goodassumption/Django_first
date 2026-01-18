import requests
import uuid, os, json, string, time
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

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
        'Authorization': os.getenv('GIGA_CHAT_AUTH')
    }
    
    # Отключение проверки SSL, если сервер в режиме разработки
    response = requests.post(url=url, headers=headers, data=payload, verify=not os.getenv('DEBUG'))
    
    # Парсим JSON и извлекаем токен
    response_data = response.json()
    access_token = response_data['access_token']
    return access_token

def make_request(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        if user_message is None:
            user_message = 'Привет! Кто ты?'
        system_prompt_ = request.POST.get('system_prompt')
        system_prompt = system_prompt_ + 'Отвечай строго в формате обычного текста без какого-либо форматирования Не используй Markdown заголовки списки жирныйкурсивный текст Emoji смайлики или символы для оформления Блоки кода с обратными кавычками HTML-теги Отступы или визуальное структурирование кроме обычных переносов строк Разделители вроде --- или *** Комментарии о формате в начале или конце ответа Все ответы должны представлять собой чистый непреформатированный текст Если нужно перечислить пункты используй простые цифры или дефисы в строку Излагай информацию максимально лаконично и по существу'

        model = "GigaChat"

        # 2. Формируем URL и заголовки для чата
        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {get_tocken()}'  # Используем вашу исправленную функцию
        }

        # 3. Формируем тело запроса в формате JSON
        payload = json.dumps({
            "model": model,  # Вы можете выбрать другую модель
            "messages": [
                {
                    'role': 'system',
                    'content': system_prompt
                },
                {
                    "role": "user",  # Роль отправителя — пользователь
                    "content": user_message  # Текст, введённый пользователем
                }
            ],
            # Опциональные параметры для настройки генерации:
            "temperature": 0.7,  # Влияет на "креативность" (от 0.0 до 1.0)
            "max_tokens": 512    # Максимальная длина ответа в токенах
        })

        response = requests.post(url, headers=headers, data=payload, verify=not os.getenv('DEBUG'))

        # 5. Обрабатываем ответ
        if response.status_code == 200:
            response_data = response.json()
            # Извлекаем текст ответа нейросети
            ai_answer = response_data['choices'][0]['message']['content']
        else:
            ai_answer = f"Ошибка: {response.status_code}. {response.text}"
    
    return {
        'model': model,
        'question': user_message,
        'ans': ai_answer,
        'system_prompt': system_prompt_,
    }

def check_spell(words):
    url = 'https://speller.yandex.net/services/spellservice.json/checkText'
    
    text = ' '.join(words)

    params = {
        'text': text
    }
    response = requests.get(url=url, params=params)

    if response.status_code != 200:
        print('Error in check_spell func')
        print('Status code:', response.status_code)
        print('Content:', response.content)
        return []

    data = response.json()
    result = []
    if data:
        for index, error in enumerate(data):
            tmp = f'{error['word']} - {error['s'][0]}'
            result.append(tmp)
        return result
            
    else:
        return []

def check_str(str):
    for char in str:
        if char.isdigit():
            return False
            
        elif char in string.punctuation and not (char == str[0] or char == str[-1]):
            return False
    
    return True

def get_weather(city):
    api = "https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=06c921750b9a82d8f5d1294e1586276f"

    json_data = requests.get(api).json()

    try:
        condition = json_data['weather'][0]['main']
        temp = int(json_data['main']['temp'] - 273.15)
        min_temp = int(json_data['main']['temp_min'] - 273.15)
        max_temp = int(json_data['main']['temp_max'] - 273.15)
        pressure = json_data['main']['pressure']
        humidity = json_data['main']['humidity']
        wind = json_data['wind']['speed']
        sunrise = time.strftime('%I:%M:%S', time.gmtime(json_data['sys']['sunrise'] - 21600))
        sunset = time.strftime('%I:%M:%S', time.gmtime(json_data['sys']['sunset'] - 21600))

        final = {
            'Условия': condition,
            'Температура': str(temp) + "°C",
            'Минимальная температура': str(min_temp) + "°C",
            'Максимальная температура': str(max_temp) + "°C",
            'Давление': str(pressure),
            'Влажность': str(humidity),
            'Скорость ветра': str(wind),
            'Время рассвета': str(sunrise),
            'Время заката': str(sunset),
        }

    except Exception as e:
        final = json_data
        final['error'] = e

    return final
