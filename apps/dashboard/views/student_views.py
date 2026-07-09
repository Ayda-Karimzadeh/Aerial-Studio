from django.views.generic import TemplateView

from apps.bookings.models import Booking
from apps.core.mixins import StudentRequiredMixin
from apps.evaluations.models import Evaluation


class StudentHomeView(StudentRequiredMixin, TemplateView):
    """داشبورد اصلی هنرجو - رزروهای فعال و آخرین ارزیابی‌ها."""
    template_name = 'dashboard/student/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upcoming_bookings'] = Booking.objects.filter(
            student=self.request.user, status='confirmed'
        ).select_related('class_session').order_by('class_session__session_date')[:5]
        context['total_bookings'] = Booking.objects.filter(student=self.request.user).count()
        context['recent_evaluations'] = Evaluation.objects.filter(
            student=self.request.user
        ).select_related('coach')[:5]
        return context
