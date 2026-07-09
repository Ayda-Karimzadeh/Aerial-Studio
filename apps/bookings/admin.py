from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_session', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('student__first_name', 'student__last_name', 'class_session__title')
    autocomplete_fields = ('student', 'class_session')
    date_hierarchy = 'created_at'
