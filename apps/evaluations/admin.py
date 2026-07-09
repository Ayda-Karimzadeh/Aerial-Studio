from django.contrib import admin
from .models import Evaluation


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('student', 'coach', 'skill_level', 'score', 'created_at')
    list_filter = ('skill_level', 'created_at')
    search_fields = ('student__first_name', 'student__last_name', 'coach__first_name', 'coach__last_name')
    autocomplete_fields = ('student', 'coach', 'class_session')
