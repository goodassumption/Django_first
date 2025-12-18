from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
import datetime

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