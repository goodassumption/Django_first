from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
import datetime
import requests
import uuid
import json

def index(request):
    context = {}
    context['author'] = 'Головин Алексей'
    context['pages'] = 1
    return render(request, 'index.html', context)

def time(request):
    context = {}
    return render(request, 'time.html', context)

def calc(request):
    context = {}
    if request.method == 'POST':
        action = request.POST.get('action', 'add')
        n1 = float(request.POST.get('first'))
        n2 = float(request.POST.get('second'))
        ans = 0.0

        match action:
            case 'sum':
                ans = n1 + n2
                context['ans'] = f'{n1} + {n2} = {str(ans)}'
            case 'sub':
                ans = n1 - n2
                context['ans'] = f'{n1} - {n2} = {str(ans)}'
            case 'mul':
                ans = n1 * n2
                context['ans'] = f'{n1} * {n2} = {str(ans)}'
            case 'div':
                if n2 == 0:
                    context['ans'] = 'На ноль делить нельзя!'
                    return render(request, 'calc.html', context)
                ans = n1 / n2
                context['ans'] = f'{n1} / {n2} = {str(ans)}'

    context['text'] = 'Итоговая операция:'
    return render(request, 'calc.html', context)

def time_update(request):
    context = {}
    now = datetime.datetime.now()
    context['date'], context['time'] = now.strftime("%Y-%m-%d %H:%M:%S").split()
    return JsonResponse(context)

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

def neyro(request):
    user_message = 'Привет! Кто ты?'
    ai_answer = ''
    if request.method == 'POST':
        user_message = request.POST.get('message')
        if user_message is None:
            user_message = 'Привет! Кто ты?'
        system_prompt_ = ''
        system_prompt = system_prompt_ + 'Отвечай строго в формате обычного текста без какого-либо форматирования Не используй Markdown заголовки списки жирныйкурсивный текст Emoji смайлики или символы для оформления Блоки кода с обратными кавычками HTML-теги Отступы или визуальное структурирование кроме обычных переносов строк Разделители вроде --- или *** Комментарии о формате в начале или конце ответа Все ответы должны представлять собой чистый непреформатированный текст Если нужно перечислить пункты используй простые цифры или дефисы в строку Излагай информацию максимально лаконично и по существу'

        # 2. Формируем URL и заголовки для чата
        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {get_tocken()}'  # Используем вашу исправленную функцию
        }

        # 3. Формируем тело запроса в формате JSON
        payload = json.dumps({
            "model": "GigaChat",  # Вы можете выбрать другую модель
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

        # 4. Отправляем POST-запрос
        response = requests.post(url, headers=headers, data=payload, verify=False)  # verify=False для разработки

        # 5. Обрабатываем ответ
        if response.status_code == 200:
            response_data = response.json()
            # Извлекаем текст ответа нейросети
            ai_answer = response_data['choices'][0]['message']['content']
        else:
            ai_answer = f"Ошибка: {response.status_code}. {response.text}"

        # 6. Передаем результат в шаблон
    content = {
        'model': 'GigaChat',
        'question': user_message,
        'ans': ai_answer,
    }
    return render(request, 'neyro.html', content)

def prompts(request):
    context = {}
    return render(request, 'prompts.html', context)