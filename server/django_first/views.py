from django.shortcuts import render

# Create your views here.

def index(request):
    context = {}
    context['author'] = 'Головин Алексей'
    context['pages'] = 1
    return render(request, 'index.html', context)