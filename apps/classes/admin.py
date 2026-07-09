from django.contrib import admin
from .models import Discipline, ClassSession


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)


@admin.register(ClassSession)
class ClassSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'discipline', 'level', 'coach', 'session_date',
                     'start_time', 'end_time', 'capacity', 'price', 'is_active')
    list_filter = ('discipline', 'level', 'is_active', 'session_date')
    search_fields = ('title', 'coach__first_name', 'coach__last_name')
    date_hierarchy = 'session_date'
    autocomplete_fields = ('coach',)
