from django.contrib import admin
from django.urls import path
from django_first import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index, name='index'),

    # ----------- ШКОЛЬНОЕ -----------
    path('time/', views.time, name = 'time'),

    path('update/time/', views.time_update, name='time_update'),

    path('calc/', views.calc, name='calc_main'),
    path('calc/simple/', views.calc_simple, name='calc'),
    path('calc/multiply/', views.multiply, name='multiply'),
    path('calc/expression/', views.expression, name='expression'),
    path('calc/expression/history/', views.expression_history, name='expression/history'),

    path('riddle/', views.riddle, name='riddle'),
    path('answer/', views.answer, name='answer'),

    path('str2words/', views.str2words, name='str2words'),

    # ----------- ЛИЧНОЕ -----------
    path('neyro/', views.neyro, name='neyro'),
    path('neyro/prompts/', views.prompts, name='prompts'),
    path('neyro/prompts/add', views.add_prompt, name='add_prompt'),

    path('viewed/', views.viewed, name='viewed'),   
    path('viewed/<str:rev_name>', views.review, name='review'),   

    path('characters/', views.characters, name='characters'),

    path('about/', views.about, name='about'),
]
