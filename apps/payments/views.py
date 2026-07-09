from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView

from apps.bookings.models import Booking
from apps.core.mixins import AdminRequiredMixin, StudentRequiredMixin
from .forms import PaymentCreateForm
from .models import Payment


class PaymentListView(AdminRequiredMixin, ListView):
    """لیست تمام پرداخت‌ها برای مدیر."""
    model = Payment
    template_name = 'payments/payment_list.html'
    context_object_name = 'payments'
    paginate_by = 15

    def get_queryset(self):
        return Payment.objects.select_related('student', 'booking__class_session')


class PaymentDetailView(DetailView):
    """جزئیات یک پرداخت مشخص."""
    model = Payment
    template_name = 'payments/payment_detail.html'
    context_object_name = 'payment'


class MyPaymentListView(StudentRequiredMixin, ListView):
    """سوابق پرداخت هنرجو."""
    model = Payment
    template_name = 'payments/my_payments.html'
    context_object_name = 'payments'
    paginate_by = 10

    def get_queryset(self):
        return Payment.objects.filter(student=self.request.user).select_related('booking__class_session')


class PaymentCreateView(AdminRequiredMixin, SuccessMessageMixin, CreateView):
    """ثبت پرداخت جدید برای یک رزرو مشخص (توسط مدیر)."""
    model = Payment
    form_class = PaymentCreateForm
    template_name = 'payments/payment_form.html'
    success_message = 'پرداخت با موفقیت ثبت شد.'

    def form_valid(self, form):
        booking = get_object_or_404(Booking, pk=self.kwargs['booking_pk'])
        form.instance.booking = booking
        form.instance.student = booking.student
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('payments:list')


class MarkPaymentPaidView(AdminRequiredMixin, View):
    """علامت‌گذاری دستی پرداخت به‌عنوان پرداخت‌شده (مثلاً پس از دریافت نقدی)."""

    def post(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        payment.mark_as_paid(gateway_ref_id=request.POST.get('gateway_ref_id', ''))
        messages.success(request, 'پرداخت با موفقیت به‌عنوان «پرداخت شده» ثبت شد.')
        return redirect('payments:list')


class RefundPaymentView(AdminRequiredMixin, View):
    """بازگشت وجه یک پرداخت."""

    def post(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        payment.refund()
        messages.success(request, 'وجه با موفقیت بازگشت داده شد.')
        return redirect('payments:list')
