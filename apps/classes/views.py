from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from apps.core.mixins import AdminRequiredMixin
from .filters import ClassSessionFilter
from .forms import ClassSessionForm
from .models import ClassSession


class ClassListView(ListView):
    """لیست عمومی کلاس‌ها (قابل مشاهده در سایت برای همه کاربران)."""
    model = ClassSession
    template_name = 'classes/class_list.html'
    context_object_name = 'classes'
    paginate_by = 9

    def get_queryset(self):
        qs = ClassSession.objects.filter(is_active=True).select_related('discipline', 'coach')
        self.filterset = ClassSessionFilter(self.request.GET, queryset=qs)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context


class ClassDetailView(DetailView):
    """جزئیات کلاس شامل ظرفیت باقی‌مانده و امکان رزرو."""
    model = ClassSession
    template_name = 'classes/class_detail.html'
    context_object_name = 'class_session'


class ClassManageListView(AdminRequiredMixin, ListView):
    """لیست مدیریتی کلاس‌ها برای مدیر (شامل غیرفعال‌ها)."""
    model = ClassSession
    template_name = 'classes/class_manage_list.html'
    context_object_name = 'classes'
    paginate_by = 15

    def get_queryset(self):
        qs = ClassSession.objects.all().select_related('discipline', 'coach')
        self.filterset = ClassSessionFilter(self.request.GET, queryset=qs)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context


class ClassCreateView(AdminRequiredMixin, SuccessMessageMixin, CreateView):
    """ایجاد کلاس جدید توسط مدیر."""
    model = ClassSession
    form_class = ClassSessionForm
    template_name = 'classes/class_form.html'
    success_url = reverse_lazy('classes:manage_list')
    success_message = 'کلاس با موفقیت ایجاد شد.'


class ClassUpdateView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):
    """ویرایش کلاس."""
    model = ClassSession
    form_class = ClassSessionForm
    template_name = 'classes/class_form.html'
    success_url = reverse_lazy('classes:manage_list')
    success_message = 'کلاس با موفقیت ویرایش شد.'


class ClassDeleteView(AdminRequiredMixin, DeleteView):
    """حذف کلاس."""
    model = ClassSession
    template_name = 'classes/class_confirm_delete.html'
    success_url = reverse_lazy('classes:manage_list')

    def form_valid(self, form):
        messages.success(self.request, 'کلاس با موفقیت حذف شد.')
        return super().form_valid(form)
