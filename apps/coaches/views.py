from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from apps.core.mixins import AdminRequiredMixin
from .forms import CoachCreateForm, CoachUpdateForm, WeeklyScheduleForm
from .models import CoachProfile


class CoachListView(ListView):
    """لیست عمومی مربیان (قابل مشاهده در صفحه Coaches سایت)."""
    model = CoachProfile
    template_name = 'coaches/coach_list.html'
    context_object_name = 'coaches'
    paginate_by = 12

    def get_queryset(self):
        return CoachProfile.objects.filter(is_active=True).select_related('user').prefetch_related('specialties')


class CoachManageListView(AdminRequiredMixin, ListView):
    """لیست مدیریتی مربیان برای مدیر (شامل غیرفعال‌ها + دکمه‌های افزودن/ویرایش/حذف)."""
    model = CoachProfile
    template_name = 'coaches/coach_manage_list.html'
    context_object_name = 'coaches'
    paginate_by = 15

    def get_queryset(self):
        return CoachProfile.objects.all().select_related('user').prefetch_related('specialties')


class CoachDetailView(DetailView):
    """مشاهده جزئیات مربی شامل تخصص، بیوگرافی و برنامه هفتگی."""
    model = CoachProfile
    template_name = 'coaches/coach_detail.html'
    context_object_name = 'coach'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schedules'] = self.object.weekly_schedules.all()
        context['classes'] = self.object.user.coached_classes.filter(is_active=True)
        return context


class CoachCreateView(AdminRequiredMixin, SuccessMessageMixin, CreateView):
    """ثبت مربی جدید توسط مدیر."""
    model = CoachProfile
    form_class = CoachCreateForm
    template_name = 'coaches/coach_form.html'
    success_url = reverse_lazy('coaches:manage_list')
    success_message = 'مربی با موفقیت ثبت شد.'


class CoachUpdateView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):
    """ویرایش اطلاعات مربی."""
    model = CoachProfile
    form_class = CoachUpdateForm
    template_name = 'coaches/coach_form.html'
    success_url = reverse_lazy('coaches:manage_list')
    success_message = 'اطلاعات مربی به‌روزرسانی شد.'


class CoachDeleteView(AdminRequiredMixin, DeleteView):
    """حذف مربی از سیستم."""
    model = CoachProfile
    template_name = 'coaches/coach_confirm_delete.html'
    success_url = reverse_lazy('coaches:manage_list')

    def form_valid(self, form):
        messages.success(self.request, 'مربی با موفقیت حذف شد.')
        return super().form_valid(form)


class WeeklyScheduleCreateView(AdminRequiredMixin, SuccessMessageMixin, CreateView):
    """افزودن برنامه هفتگی برای یک مربی مشخص."""
    form_class = WeeklyScheduleForm
    template_name = 'coaches/schedule_form.html'
    success_message = 'برنامه هفتگی افزوده شد.'

    def form_valid(self, form):
        form.instance.coach_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('coaches:detail', kwargs={'pk': self.kwargs['pk']})