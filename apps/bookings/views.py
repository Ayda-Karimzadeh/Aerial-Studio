from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView, TemplateView

from apps.classes.models import ClassSession
from apps.core.mixins import StudentRequiredMixin
from .forms import BookingCancelForm
from .models import Booking


class ClassCalendarView(StudentRequiredMixin, TemplateView):
    """نمایش تقویم کلاس‌های قابل رزرو برای هنرجو."""
    template_name = 'bookings/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classes'] = ClassSession.objects.filter(is_active=True).select_related('discipline', 'coach')
        context['my_booked_ids'] = set(
            Booking.objects.filter(
                student=self.request.user, status__in=['pending', 'confirmed']
            ).values_list('class_session_id', flat=True)
        )
        return context


class BookingCreateView(StudentRequiredMixin, View):
    """رزرو یک کلاس مشخص توسط هنرجو."""

    def post(self, request, class_pk):
        class_session = get_object_or_404(ClassSession, pk=class_pk, is_active=True)

        if Booking.objects.filter(student=request.user, class_session=class_session).exclude(
            status='cancelled'
        ).exists():
            messages.warning(request, 'شما قبلاً این کلاس را رزرو کرده‌اید.')
            return redirect('bookings:calendar')

        if class_session.is_full:
            messages.error(request, 'ظرفیت این کلاس تکمیل شده است.')
            return redirect('bookings:calendar')

        booking = Booking(student=request.user, class_session=class_session, status=Booking.Status.CONFIRMED)
        try:
            booking.full_clean()
            booking.save()
            messages.success(request, f'رزرو کلاس «{class_session.title}» با موفقیت انجام شد.')
        except ValidationError as e:
            messages.error(request, ' '.join(e.messages))

        return redirect('bookings:calendar')


class BookingListView(StudentRequiredMixin, ListView):
    """سوابق رزرو هنرجو."""
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'
    paginate_by = 10

    def get_queryset(self):
        return Booking.objects.filter(student=self.request.user).select_related('class_session', 'class_session__discipline')


class BookingDetailView(StudentRequiredMixin, DetailView):
    """جزئیات یک رزرو مشخص."""
    model = Booking
    template_name = 'bookings/booking_detail.html'
    context_object_name = 'booking'

    def get_queryset(self):
        return Booking.objects.filter(student=self.request.user)


class BookingCancelView(StudentRequiredMixin, View):
    """لغو رزرو توسط هنرجو."""

    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk, student=request.user)
        if booking.status in ['cancelled', 'completed']:
            messages.warning(request, 'این رزرو قابل لغو نیست.')
            return redirect('bookings:list')

        reason = request.POST.get('cancellation_reason', '')
        booking.cancel(reason=reason)
        messages.success(request, 'رزرو با موفقیت لغو شد.')
        return redirect('bookings:list')
