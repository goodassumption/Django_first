from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from django_first.models import *
from django_first.forms import *

import datetime, json
from random import randint

from .utilits import make_request, check_str, check_spell

def index(request):
    context = {
        'pages': list(PagesModel.objects.values())
    }
    
    return render(request, 'index.html', context)

# ------------- ВРЕМЯ ------------- 
def time(request):
    return render(request, 'time.html')

def time_update(request):
    # Получаем часовой пояс из GET параметра
    timezone_str = request.GET.get('timezone')
    default_hours = 0
    
    if timezone_str:
        try:
            hours = float(timezone_str)
        except (ValueError, TypeError):
            hours = default_hours
    else:
        hours = default_hours
    
    delta = datetime.timedelta(hours=hours)
    now = datetime.datetime.now() + delta

    return JsonResponse({
        'date': now.strftime("%d-%m-%Y"),
        'time': now.strftime("%H:%M:%S"),
    })

# ------------- КАЛЬКУЛЯТОРЫ ------------- 
def calc(request):
    return render(request, 'calc_main.html')

def calc_simple(request):
    action = 'sum'
    n1 = randint(1, 44)
    n2 = randint(1, 66)
    
    context = {
        'n1': n1,
        'n2': n2,
    }

    if request.method == 'POST':
        action = request.POST.get('action', 'add')
        
        try:
            n1 = int(request.POST.get('first'))
        except:
            n1 = float(request.POST.get('first'))

        try:
            n2 = int(request.POST.get('second'))
        except:
            n2 = float(request.POST.get('second'))

    ans = None
    if action == 'sum':
        ans = n1 + n2
        expr = f'{n1} + {n2}'
        context['ans'] = f'{expr} = {str(ans)}'
    elif action == 'sub':
        ans = n1 - n2
        expr = f'{n1} - {n2}'
        context['ans'] = f'{expr} = {str(ans)}'
    elif action == 'mul':
        ans = n1 * n2
        expr = f'{n1} * {n2}'
        context['ans'] = f'{expr} = {str(ans)}'
    elif action == 'div':
        if n2 == 0:
            context['ans'] = 'На ноль делить нельзя!'
            return render(request, 'calc.html', context)
        ans = n1 / n2
        expr = f'{n1} / {n2}'
        context['ans'] = f'{expr} = {str(ans)}'

    obj = CalcHistory(
            expression=expr,
            result=ans,
            time=create_time(),
            expr_type='Простая операция'
        )
    obj.save()

    context['text'] = 'Итоговая операция:'
    return render(request, 'calc.html', context)

def expression(request):
    context = {
        'expression': f'{randint(1, 99)} + {randint(1, 99)} - {randint(1, 99)}'
    }

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
            obj = CalcHistory(
                expression=expr_,
                result=answer,
                time=create_time(),
                expr_type='Сложная операция'
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

def expression_history(request):
    history = CalcHistory.objects.all().order_by('-time')
    
    context = {
        'complex_history': history.filter(expr_type="Сложная операция"),
        'simple_history': history.filter(expr_type="Простая операция"),
    }
    return render(request, 'history.html', context)

def multiply(request):
    context = {
        'n1': 1,
        'n2': 10,
    }

    if request.method == 'POST':
        try:
            try:
                n1 = int(request.POST.get('num1'))
            except:
                n1 = float(request.POST.get('num1'))
            n2 = int(request.POST.get('num2'))
            context['n1'] = n1
            context['n2'] = n2
        except Exception as e:
            print(e)
            context['error'] = f'Информация об ошибке: {e}'
            return render(request, 'multiply.html', context)

    smth = []
    for i in range(context['n2']+1):
        smth.append(
            f'{context['n1']} * {i} = {round(context['n1']*i, 4)}'
        )
    context['ans'] = smth
    return render(request, 'multiply.html', context)

# ------------- СТРОКИ -------------
def str2words(request):
    context = {}

    if request.method == 'POST':
        form = Str2WordsForm(request.POST)

        if form.is_valid():
            model = form.save(commit=False)

            original_text = list(dict(request.POST).values())[1][0]
            answer = original_text.split()

            digits = []
            words = []
            others = []

            for item in answer:
                if item.isdigit():
                    digits.append(item)

                elif check_str(item):
                    words.append(item)

                else:
                    others.append(item)

            errors = check_spell(words)

            model.original_text = original_text
            model.digits = digits
            model.words = words
            model.errors = errors
            model.others = others
            model.save()

            context = {
                'answer': original_text,
                'digits': digits,
                'words': words,
                'others': others,
                'errors': errors,
            }

    context['form'] = Str2WordsForm()

    return render(request, 'str2words.html', context)

def str2words_history(request):
    context = {
        'ans': list(StrHistory.objects.values()),   
        'is_auth': request.user.is_authenticated
    }

    return render(request, 'str2words_history.html', context)

def str2words_history_more(request, str_id):
    context = {
        'answer': StrHistory.objects.values_list('original_text').filter(id=str_id)[0],
        'digits': StrHistory.objects.values_list('digits').filter(id=str_id)[0][0],
        'words': StrHistory.objects.values_list('words').filter(id=str_id)[0][0],
        'others': StrHistory.objects.values_list('others').filter(id=str_id)[0][0],
        'errors': StrHistory.objects.values_list('errors').filter(id=str_id)[0][0],
    }

    return render(request, 'str2words_history_more.html', context)

# ------------- НЕЙРОСЕТИ ------------- 
def neyro(request):
    if request.method == 'POST':
        context = make_request(request)

    else:
        context = {
        'model': 'GigaChat',
        'question': 'Привет! Кто ты?',
        }

    return render(request, 'neyro.html', context)

def prompts(request):
    context = {
        'prompts': list(PromptsModel.objects.values('name', 'prompt', 'description').filter(is_approved=True))
    }

    return render(request, 'prompts.html', context)

def add_prompt(request):
    if request.method == 'POST':
        form = AddPromptForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_prompt')
    
    else:
        form = AddPromptForm(data=None)


    context = {
        'form': form,
    }

    return render(request, 'add_prompt.html', context) 

# ------------- ЗАГАДКА/ОТГАДКА ------------- 
def riddle(request):
    return render(request, 'riddle.html')

def answer(request):
    return render(request, 'answer.html')

def viewed(request):
    all = list(ReviewModel.objects.values())

    context = {
        'data': all
    }
    
    return render(request, 'viewed.html', context)

# ------------- ИНФОРМАЦИОННЫЕ СТРАНИЦЫ ------------- 
def review(request, rev_name):
    context = {
        'name': ReviewModel.objects.values_list('name').filter(name=rev_name),
        'review': ReviewModel.objects.values_list('review').filter(name=rev_name),
    }

    return render(request, 'review.html', context)

def characters(request):
    context = {
        'media_list': list(CharactersModel.objects.values()),
    }

    return render(request, 'characters.html', context)

def about(request):
    context = {
        'social': list(SocialsModel.objects.values()),
        'refs': list(RefsModel.objects.values()),
        'games': list(GamesModel.objects.values()),
        'hobbies': list(HobbyModel.objects.values()),
        'preformers': list(PreformersModel.objects.values()),
    }

    return render(request, 'about.html', context)
