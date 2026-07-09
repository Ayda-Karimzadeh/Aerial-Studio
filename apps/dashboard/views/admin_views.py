from django.views.generic import TemplateView

from apps.bookings.models import Booking
from apps.classes.models import ClassSession
from apps.core.mixins import AdminRequiredMixin
from apps.payments.models import Payment
from apps.reports import services


class AdminHomeView(AdminRequiredMixin, TemplateView):
    """داشبورد اصلی مدیر - آمار کلی، کارت‌ها و فعالیت‌های اخیر."""
    template_name = 'dashboard/admin/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(services.get_dashboard_stats())
        context['recent_bookings'] = Booking.objects.select_related(
            'student', 'class_session'
        ).order_by('-created_at')[:5]
        context['recent_payments'] = Payment.objects.select_related(
            'student'
        ).order_by('-created_at')[:5]
        context['upcoming_classes'] = ClassSession.objects.filter(is_active=True).order_by('session_date')[:5]
        return context
