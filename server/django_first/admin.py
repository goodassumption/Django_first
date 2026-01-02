from django.contrib import admin
from .models import *

@admin.register(CalcHistory)
class CalcHistoryAdmin(admin.ModelAdmin):
    list_display = ('expression', 'result', 'time')
    list_filter = ('time',)
    search_fields = ('expression',)

@admin.register(CharactersModel)
class CharactersModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'time')
    list_filter = ('name',)
    search_fields = ('name',)

@admin.register(ReviewModel)
class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'time')
    search_fields = ('name',)
    list_filter = ('name',)

@admin.register(RefsModel)
class SocialsModelAdmin(admin.ModelAdmin):
    list_display = ('author', 'img_url')
    search_fields = ('author',)
    list_filter = ('author',)

@admin.register(SocialsModel)
class SocialsModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    search_fields = ('name',)
    list_filter = ('name',)

@admin.register(GamesModel)
class GamesModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    search_fields = ('name',)
    list_filter = ('name',)

@admin.register(HobbyModel)
class HobbyModelAdmin(admin.ModelAdmin):
    pass
