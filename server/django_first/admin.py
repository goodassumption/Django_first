from django.contrib import admin
from .models import *

# Модели без кастомизации
admin.site.register(HobbyModel)
admin.site.register(PreformersModel)

@admin.register(CalcHistory)
class CalcHistoryAdmin(admin.ModelAdmin):
    list_display = ('expression', 'result', 'time')
    search_fields = ('expression',)

@admin.register(CharactersModel)
class CharactersModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    search_fields = ('name',)

@admin.register(ReviewModel)
class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'review_time')
    search_fields = ('name',)

@admin.register(RefsModel)
class RefsModelAdmin(admin.ModelAdmin):
    list_display = ('author','character' ,'img_url')
    search_fields = ('author',)
    list_filter = ('author',)

@admin.register(SocialsModel)
class SocialsModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    search_fields = ('name',)

@admin.register(GamesModel)
class GamesModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    search_fields = ('name',)

@admin.register(PagesModel)
class PagesModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    search_fields = ('name',)

@admin.register(PromptsModel)
class PromptsModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_approved')
    search_fields = ('name',)
    list_filter = ('is_approved',)

@admin.register(StrHistory)
class StrHistoryAdmin(admin.ModelAdmin):
    list_display = ('original_text', 'time')

@admin.register(RandomModel)
class RandomModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'link')
