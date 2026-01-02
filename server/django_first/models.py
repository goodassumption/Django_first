from django.db import models
from datetime import datetime

def create_time():
    now = datetime.now()
    return now.strftime("%d-%m-%Y %H:%M:%S")

class CalcHistory(models.Model):
    expression = models.CharField(max_length=100)
    result = models.IntegerField()
    time = models.CharField(max_length=500)
    
    # Для красивого отображения в админке и shell
    def __str__(self):
        return f"{self.expression} = {self.result}"
    
    # Мета-класс для настроек
    class Meta:
        verbose_name = "История вычислений"
        verbose_name_plural = "История вычислений"
        ordering = ['-time']  # сортировка по убыванию времени

class CharactersModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя персонажа')
    url = models.CharField(max_length=100, verbose_name='Ссылка на картинку')
    time = models.CharField(max_length=50, default=create_time(), editable=False, verbose_name='Время создания')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Персонаж"
        verbose_name_plural = "Персонажи"

class ReviewModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название фильма')
    review = models.TextField(verbose_name='Рецензия')
    url = models.CharField(max_length=100, default='', verbose_name='Ссылка на постер')
    time = models.CharField(max_length=50, default=create_time(), editable=False, verbose_name='Время создания')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Рецензия"
        verbose_name_plural = "Рецензии"    

class RefsModel(models.Model):
    img_url = models.CharField(max_length=100, verbose_name='Ссылка на арт')
    channel = models.CharField(max_length=100, verbose_name='Ссылка на художника')
    author = models.CharField(max_length=100, verbose_name='Ник художника')

    def __str__(self):
        return self.author
    
    class Meta:
        verbose_name = 'Референс'
        verbose_name_plural = 'Референсы'

class SocialsModel(models.Model):
    url = models.CharField(max_length=100, verbose_name='Ссылка на соцсеть')
    name = models.CharField(max_length=100, verbose_name='Название соцсети')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Ссылка на соцсеть'
        verbose_name_plural = 'Ссылки на соцсети'

class GamesModel(models.Model):
    url = models.CharField(max_length=100, default='', verbose_name='Ссылка на игру в стиме')
    name = models.CharField(max_length=100, verbose_name='Название игры')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'

# Это тупизм, у меня едет крыша
class HobbyModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='Увлечение')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Увлечение'
        verbose_name_plural = 'Увлечения'

