from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django_first.models import CalcHistory

import datetime, os, uuid, json, random
import requests

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
        if action ==  'sum':
            ans = n1 + n2
            context['ans'] = f'{n1} + {n2} = {str(ans)}'
        elif action ==  'sub':
            ans = n1 - n2
            context['ans'] = f'{n1} - {n2} = {str(ans)}'
        elif action ==  'mul':
            ans = n1 * n2
            context['ans'] = f'{n1} * {n2} = {str(ans)}'
        elif action ==  'div':
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

    # let's go gambling!
    rnd = random.randint(0, 1000000)
    if rnd % 2 == 0:
        if rnd % 3 == 0:
            context['date'], context['time'] = now.strftime("%m-%Y-%d %H:%M:%S").split()
        else:
            context['date'], context['time'] = now.strftime("%Y-%m-%d %H:%M:%S").split()
    else:
        if rnd % 3 == 0:
            context['date'], context['time'] = now.strftime("%m-%d-%Y %H:%M:%S").split()
        else:
            context['date'], context['time'] = now.strftime("%d-%m-%Y %H:%M:%S").split()
    
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

def riddle(request):
    context = {}
    return render(request, 'riddle.html', context)

def answer(request):
    context = {}
    return render(request, 'answer.html', context)

def multiply(request):
    context ={
        'ans': ['1 * 0 = 0', '1 * 1 = 1', '1 * 2 = 2', '1 * 3 = 3', '1 * 4 = 4', '1 * 5 = 5', '1 * 6 = 6', '1 * 7 = 7', '1 * 8 = 8', '1 * 9 = 9', '1 * 10 = 10'],
        'n1': 1,
        'n2': 10,
    }
    if request.method == 'POST':
        try:
            n1 = int(request.POST.get('num1'))
            n2 = int(request.POST.get('num2'))
        except Exception as e:
            print(e)
            context['ans'] = f'ОШИБКА: {e}'
            return render(request, 'multiply.html', context)
    
        smth = []
        for i in range(n2+1):
            smth.append(
                f'{n1} * {i} = {n1*i}'
            )
        context['ans'] = smth
        context['n1'] = n1
        context['n2'] = n2

    return render(request, 'multiply.html', context)

def anime(request):
    return render(request, 'anime.html', {})

def characters(request):
    context = {
        'media_list': scan_kinns_folder(),
    }
    return render(request, 'kinns.html', context)

def expression(request):
    context = {}
    if request.method == 'POST':
        expr_ = request.POST.get('expression')
        
        # Проверка на пустое выражение
        if not expr_:
            context['error'] = 'Выражение не может быть пустым'
            return render(request, 'expression.html', context)
            
        try:
            expr = expr_.split()
            
            # Проверка минимальной длины выражения
            if len(expr) < 3 or len(expr) % 2 == 0:
                context['error'] = 'Неверный формат выражения. Пример: "5 + 3 - 2"'
                context['expression'] = expr_
                return render(request, 'expression.html', context)
            
            context['expression'] = expr_
            
            # Начальное значение - первое число
            try:
                answer = int(expr[0])
            except ValueError:
                context['error'] = 'Первым элементом должно быть число'
                return render(request, 'expression.html', context)
            
            # Обработка операций
            for i in range(1, len(expr), 2):
                # Проверка, что на позиции оператора действительно оператор
                if expr[i] not in ('+', '-'):
                    context['error'] = f'Неверный оператор: {expr[i]}'
                    return render(request, 'expression.html', context)
                
                # Проверка, что после оператора идет число
                if i + 1 >= len(expr):
                    context['error'] = 'Выражение завершается оператором'
                    return render(request, 'expression.html', context)
                
                try:
                    num = int(expr[i + 1])
                except ValueError:
                    context['error'] = f'Ожидалось число после оператора, получено: {expr[i + 1]}'
                    return render(request, 'expression.html', context)
                
                # Выполнение операции
                if expr[i] == '+':
                    answer += num
                elif expr[i] == '-':
                    answer -= num
            
            context['answer'] = answer
            context['error'] = None
            
            # Сохранение в историю (исправлен формат времени)
            now = datetime.datetime.now()
            obj = CalcHistory(
                expression=expr_,
                result=answer,
                time=now.strftime("%d-%m-%Y %H:%M:%S")  # Используйте strftime вместо strptime
            )
            obj.save()

        except Exception as e:
            print(f"Error: {e}")
            # Правильная проверка типа исключения
            if isinstance(e, ZeroDivisionError):
                context['error'] = 'Деление на ноль'
            elif isinstance(e, ValueError):
                context['error'] = 'Ошибка значения. Проверьте ввод чисел'
            elif isinstance(e, TypeError):
                context['error'] = 'Ошибка типа данных'
            elif isinstance(e, IndexError):
                context['error'] = 'Неполное выражение'
            else:
                context['error'] = f'Ошибка: {str(e)}'
            
            # Сохраняем выражение даже при ошибке
            context['expression'] = expr_

    return render(request, 'expression.html', context)

def history(request):
    history = list(CalcHistory.objects.values('expression', 'result', 'time'))
    context = {
        'history': history
    }
    return render(request, 'history.html', context)

def scan_kinns_folder():
    """
    Функция для автоматического сканирования папки kinns
    """
    media_list = []
    
    try:
        # Путь к вашей папке kinns
        kinns_path = os.path.join(settings.STATICFILES_DIRS[0], 'media', 'kinns')
        
        if os.path.exists(kinns_path):
            for filename in os.listdir(kinns_path):
                # Проверяем расширения файлов
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')):
                    media_list.append({
                        'type': 'photo',
                        'title': get_nice_filename(filename),
                        'url': f'media/kinns/{filename}',  # Правильный путь
                        'description': f'Фото из коллекции',
                    })
                elif filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm')):
                    media_list.append({
                        'type': 'video',
                        'title': get_nice_filename(filename),
                        'url': f'media/kinns/{filename}',  # Правильный путь
                        'description': f'Видео из коллекции',
                        'duration': '2:00'
                    })
        else:
            print(f"Папка не найдена: {kinns_path}")
            
    except Exception as e:
        print(f"Ошибка сканирования папки: {e}")
    
    return media_list

def get_nice_filename(filename):
    """
    Преобразует имя файла в читаемый формат
    Пример: "my_photo_2023.jpg" -> "My Photo 2023"
    """
    name = os.path.splitext(filename)[0]
    # Заменяем подчеркивания и дефисы на пробелы
    name = name.replace('_', ' ').replace('-', ' ')
    # Делаем первую букву каждого слова заглавной
    return ' '.join(word.capitalize() for word in name.split())   
