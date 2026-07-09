from django.views.generic import TemplateView

from apps.core.mixins import AdminRequiredMixin
from . import services
from .charts import get_revenue_chart_data, get_discipline_chart_data


class ReportsView(AdminRequiredMixin, TemplateView):
    """صفحه گزارش‌گیری کامل برای مدیر - آمار کلی، نمودارها و لیست کلاس‌ها."""
    template_name = 'dashboard/admin/reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        full_classes, empty_classes = services.get_full_and_empty_classes()

        context.update(services.get_dashboard_stats())
        context['popular_discipline'] = services.get_popular_discipline()
        context['full_classes'] = full_classes
        context['empty_classes'] = empty_classes
        context['revenue_chart_data'] = get_revenue_chart_data()
        context['discipline_chart_data'] = get_discipline_chart_data()
        return context
