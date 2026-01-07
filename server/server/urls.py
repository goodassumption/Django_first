from django.contrib import admin
from django.urls import path
from django_first import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('time/', views.time, name = 'time'),
    path('update/time/', views.time_update, name='time_update'),
    path('calc/', views.calc, name='calc'),
    path('neyro/', views.neyro, name='neyro'),
    path('neyro/prompts/', views.prompts, name='prompts'),
    path('neyro/prompts/add', views.add_prompt, name='add_prompt'),
    path('riddle/', views.riddle, name='riddle'),
    path('answer/', views.answer, name='answer'),
    path('multiply/', views.multiply, name='multiply'),
    path('viewed/', views.viewed, name='viewed'),   
    path('viewed/<str:rev_name>', views.review, name='review'),   
    path('characters/', views.characters, name='characters'),
    path('expression/', views.expression, name='expression'),
    path('expression/history/', views.history, name='history'),
    path('about/', views.about, name='about'),
]
