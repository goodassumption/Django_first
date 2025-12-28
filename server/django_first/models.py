from django.db import models

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