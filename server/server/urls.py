"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django_first import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('time/', views.time, name = 'time'),
    path('update/', views.time_update, name='update'),
    path('calc/', views.calc, name='calc'),
    path('neyro/', views.neyro, name='neyro'),
    path('neyro/prompts/', views.prompts, name='prompts'),
    path('riddle/', views.riddle, name='riddle'),
    path('answer/', views.answer, name='answer'),
    path('multiply/', views.multiply, name='multiply'),
    path('anime/', views.anime, name='anime'),
    path('characters/', views.characters, name='characters'),
    path('expression/', views.expression, name='expression'),
    path('expression/history/', views.history, name='history'),

]
