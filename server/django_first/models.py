from django.db import models

from .utilits import create_time

class CalcHistory(models.Model):
    expression = models.CharField(max_length=100, verbose_name='Исходное выражение')
    result = models.IntegerField(verbose_name='Результат операции')
    time = models.CharField(max_length=50, default=create_time(), editable=False, verbose_name='Время создания')
    
    def __str__(self):
        return f"{self.expression} = {self.result}"
    
    class Meta:
        verbose_name = "История вычислений"
        verbose_name_plural = "История вычислений"
        ordering = ['-time']

class CharactersModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя персонажа')
    url = models.CharField(max_length=100, verbose_name='Ссылка на картинку')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Персонаж"
        verbose_name_plural = "Персонажи"

class ReviewModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    review = models.TextField(verbose_name='Текст рецензии', default='', blank=True, null=True)
    review_time = models.CharField(max_length=50, default=create_time()[:-9], verbose_name='Дата создания рецензии')
    genre = models.CharField(
        verbose_name='Жанр',
        choices={
            'Аниме': 'Аниме',
            'Фильм': 'Фильм',
            'Сериал': 'Сериал',
            'Мультик': 'Мультик',
        },
        null=True
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Рецензия"
        verbose_name_plural = "Рецензии"    

class RefsModel(models.Model):
    img_url = models.CharField(max_length=100, verbose_name='Ссылка на арт')
    channel = models.CharField(max_length=100, verbose_name='Ссылка на художника')
    author = models.CharField(max_length=100, verbose_name='Ник художника')
    character = models.CharField(
        max_length=100,
        choices=[
            ('1', 'Селфсона'),
            ('2', 'Старый скин'),
        ],
        default='Undefined',
        verbose_name='Имя ОС-а',
    )

    def __str__(self):
        return self.author
    
    class Meta:
        verbose_name = 'Референс'
        verbose_name_plural = 'Референсы'

class SocialsModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название соцсети')
    url = models.CharField(max_length=100, verbose_name='Ссылка на соцсеть')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Ссылка на соцсеть'
        verbose_name_plural = 'Ссылки на соцсети'

class GamesModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название игры')
    url = models.CharField(max_length=100, default='', verbose_name='Ссылка на игру')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'

class HobbyModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='Увлечение')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Увлечение'
        verbose_name_plural = 'Увлечения'

class PreformersModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='Исполнитель')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'

class PagesModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название страницы')
    url = models.CharField(max_length=100, verbose_name='Путь относительно главной')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'

class PromptsModel(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название промпта')
    prompt = models.TextField(verbose_name='Промпт')
    description = models.CharField(max_length=100, verbose_name='Описание промпта')
    is_approved = models.BooleanField(verbose_name='Статус одобрения', default=False)
    created_at = models.CharField(max_length=50, default=create_time(), verbose_name='Время отправки промпта')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Промпт'
        verbose_name_plural='Промпты'
