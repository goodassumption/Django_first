from django.contrib import admin
from django.urls import path
from django_first import views

urlpatterns = [
    # ----------- АДМИНКА -----------
    path('admin/', admin.site.urls),

    # ----------- ГЛАВНАЯ -----------
    path('', views.index, name='index'),

    # ----------- БЕСПОЛЕЗНОЕ -----------
    path('time/', views.time, name = 'time'),
    path('weather/', views.weather, name='weather'),

    # ----------- ОБНОВЛЕНИЕ ДАННЫХ -----------
    path('update/time/', views.time_update, name='time_update'),

    # ----------- КАЛЬКУЛЯТОРЫ -----------
    path('calc/', views.calc, name='calc_main'),
    path('calc/simple/', views.calc_simple, name='calc'),
    path('calc/multiply/', views.multiply, name='multiply'),
    path('calc/expression/', views.expression, name='expression'),
    path('calc/expression/history/', views.expression_history, name='expression/history'),

    # ----------- ЗАГАДКИ -----------
    path('riddle/', views.riddle, name='riddle'),
    path('answer/', views.answer, name='answer'),

    # ----------- СТРОКИ -----------
    path('str2words/', views.str2words, name='str2words'),
    path('str2words/history/', views.str2words_history, name='str2words/history'),
    path('str2words/history/<int:str_id>', views.str2words_history_more, name='str2words/history/more'),

    # ----------- ПРОСМОТРЕННОЕ -----------
    path('viewed/', views.viewed, name='viewed'),   
    path('viewed/<str:rev_name>', views.review, name='review'),   

    # ----------- ПЕРСОНАЖИ -----------
    path('characters/', views.characters, name='characters'),

    # ----------- ОБО МНЕ -----------
    path('about/', views.about, name='about'),

    # ----------- РАНДОМ -----------
    path('random/', views.random, name='random'),

    # ----------- РЕДИРЕКТЫ -----------
    path('r/<str:service_name>', views.redirects, name='redirects'),
    
]