from django.views.generic import TemplateView

from apps.classes.models import ClassSession
from apps.core.mixins import CoachRequiredMixin
from apps.evaluations.models import Evaluation


class CoachHomeView(CoachRequiredMixin, TemplateView):
    """داشبورد اصلی مربی - کلاس‌های تخصیص یافته و ارزیابی‌های اخیر."""
    template_name = 'dashboard/coach/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_classes = ClassSession.objects.filter(coach=self.request.user).select_related('discipline')
        context['my_classes'] = my_classes.order_by('session_date')[:6]
        context['total_classes'] = my_classes.count()
        context['recent_evaluations'] = Evaluation.objects.filter(
            coach=self.request.user
        ).select_related('student')[:5]
        return context
