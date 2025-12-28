from django.contrib import admin
from .models import CalcHistory

@admin.register(CalcHistory)
class CalcHistoryAdmin(admin.ModelAdmin):
    list_display = ('expression', 'result', 'time')  # что показывать в списке
    list_filter = ('time',)  # фильтры справа
    search_fields = ('expression',)  # поиск по выражению