from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from apps.core.mixins import CoachRequiredMixin, StudentRequiredMixin
from .forms import EvaluationForm
from .models import Evaluation


class EvaluationCreateView(CoachRequiredMixin, SuccessMessageMixin, CreateView):
    """ثبت ارزیابی جدید توسط مربی برای یک هنرجو."""
    model = Evaluation
    form_class = EvaluationForm
    template_name = 'dashboard/coach/evaluation_form.html'
    success_url = reverse_lazy('evaluations:coach_list')
    success_message = 'ارزیابی با موفقیت ثبت شد.'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['coach'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.coach = self.request.user
        return super().form_valid(form)


class CoachEvaluationListView(CoachRequiredMixin, ListView):
    """لیست ارزیابی‌های ثبت‌شده توسط مربی."""
    model = Evaluation
    template_name = 'dashboard/coach/evaluation_list.html'
    context_object_name = 'evaluations'
    paginate_by = 10

    def get_queryset(self):
        return Evaluation.objects.filter(coach=self.request.user).select_related('student', 'class_session')


class StudentEvaluationListView(StudentRequiredMixin, ListView):
    """لیست ارزیابی‌های دریافتی هنرجو."""
    model = Evaluation
    template_name = 'dashboard/student/evaluation_list.html'
    context_object_name = 'evaluations'
    paginate_by = 10

    def get_queryset(self):
        return Evaluation.objects.filter(student=self.request.user).select_related('coach', 'class_session')


class EvaluationDetailView(DetailView):
    """جزئیات یک ارزیابی مشخص."""
    model = Evaluation
    template_name = 'dashboard/evaluation_detail.html'
    context_object_name = 'evaluation'
