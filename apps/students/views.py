from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from apps.core.mixins import AdminRequiredMixin, AdminOrCoachRequiredMixin
from apps.bookings.models import Booking
from apps.evaluations.models import Evaluation
from .filters import StudentFilter
from .forms import StudentCreateForm, StudentUpdateForm
from .models import StudentProfile


class StudentListView(AdminOrCoachRequiredMixin, ListView):
    """لیست کامل هنرجویان همراه با جستجو و فیلتر."""
    model = StudentProfile
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    paginate_by = 12

    def get_queryset(self):
        qs = StudentProfile.objects.select_related('user').all()
        self.filterset = StudentFilter(self.request.GET, queryset=qs)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context


class StudentDetailView(AdminOrCoachRequiredMixin, DetailView):
    """مشاهده پروفایل کامل هنرجو، سوابق کلاس‌ها و ارزیابی‌ها."""
    model = StudentProfile
    template_name = 'students/student_detail.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_user = self.object.user
        context['bookings'] = Booking.objects.filter(student=student_user).select_related('class_session')
        context['evaluations'] = Evaluation.objects.filter(student=student_user).select_related('coach')
        return context


class StudentCreateView(AdminRequiredMixin, SuccessMessageMixin, CreateView):
    """ثبت هنرجوی جدید توسط مدیر."""
    model = StudentProfile
    form_class = StudentCreateForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:list')
    success_message = 'هنرجو با موفقیت ثبت شد.'


class StudentUpdateView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):
    """ویرایش اطلاعات هنرجو."""
    model = StudentProfile
    form_class = StudentUpdateForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:list')
    success_message = 'اطلاعات هنرجو به‌روزرسانی شد.'


class StudentDeleteView(AdminRequiredMixin, DeleteView):
    """حذف هنرجو از سیستم."""
    model = StudentProfile
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('students:list')

    def form_valid(self, form):
        messages.success(self.request, 'هنرجو با موفقیت حذف شد.')
        return super().form_valid(form)
