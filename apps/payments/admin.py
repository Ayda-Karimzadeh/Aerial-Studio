from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('tracking_code', 'student', 'booking', 'amount', 'method', 'status', 'paid_at')
    list_filter = ('status', 'method')
    search_fields = ('tracking_code', 'student__first_name', 'student__last_name', 'gateway_ref_id')
    autocomplete_fields = ('student', 'booking')
    readonly_fields = ('tracking_code',)
