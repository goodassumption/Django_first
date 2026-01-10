from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django_first.models import *
from django_first.forms import *

import datetime
from random import randint

from .utilits import make_request

def index(request):
    context = {
        'pages': list(PagesModel.objects.values())
    }
    
    return render(request, 'index.html', context)

def time(request):
    return render(request, 'time.html')

def time_update(request):
    now = datetime.datetime.now()

    context = {
        'date': now.strftime("%d-%m-%Y"),
        'time': now.strftime("%H:%M:%S"),
    }
    
    return JsonResponse(context)

def calc(request):
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

def riddle(request):
    return render(request, 'riddle.html')

def answer(request):
    return render(request, 'answer.html')

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

def viewed(request):
    all = list(ReviewModel.objects.values())

    context = {
        'data': all
    }
    
    return render(request, 'viewed.html', context)

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

def history(request):
    history = CalcHistory.objects.all().order_by('-time')
    
    context = {
        'complex_history': history.filter(expr_type="Сложная операция"),
        'simple_history': history.filter(expr_type="Простая операция"),
    }
    return render(request, 'history.html', context)

def about(request):
    context = {
        'social': list(SocialsModel.objects.values()),
        'refs': list(RefsModel.objects.values()),
        'games': list(GamesModel.objects.values()),
        'hobbies': list(HobbyModel.objects.values()),
        'preformers': list(PreformersModel.objects.values()),
    }

    return render(request, 'about.html', context)
