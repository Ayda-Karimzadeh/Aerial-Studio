from django.contrib import admin
from .models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'membership_status', 'level', 'joined_date')
    list_filter = ('membership_status', 'level')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    autocomplete_fields = ('user',)
