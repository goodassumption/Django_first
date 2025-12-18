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

def time_update(request):
    context = {}
    now = datetime.datetime.now()
    context['date'], context['time'] = now.strftime("%Y-%m-%d %H:%M:%S").split()
    return JsonResponse(context)

def calc(request):
    context = {}
    return render(request, 'calc.html', context)
