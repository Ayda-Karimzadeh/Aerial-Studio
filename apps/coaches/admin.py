from django.contrib import admin
from .models import CoachProfile, WeeklySchedule


class WeeklyScheduleInline(admin.TabularInline):
    model = WeeklySchedule
    extra = 1


@admin.register(CoachProfile)
class CoachProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'years_of_experience', 'is_active')
    list_filter = ('is_active', 'specialties')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    filter_horizontal = ('specialties',)
    autocomplete_fields = ('user',)
    inlines = [WeeklyScheduleInline]


@admin.register(WeeklySchedule)
class WeeklyScheduleAdmin(admin.ModelAdmin):
    list_display = ('coach', 'weekday', 'start_time', 'end_time')
    list_filter = ('weekday',)
