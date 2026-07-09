from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from apps.core.models import TimeStampedModel


class Booking(TimeStampedModel):
    """رزرو کلاس توسط هنرجو."""

    class Status(models.TextChoices):
        PENDING = 'pending', 'در انتظار تایید'
        CONFIRMED = 'confirmed', 'تایید شده'
        CANCELLED = 'cancelled', 'لغو شده'
        COMPLETED = 'completed', 'برگزار شده'

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='bookings', limit_choices_to={'role': 'student'}, verbose_name='هنرجو'
    )
    class_session = models.ForeignKey(
        'classes.ClassSession', on_delete=models.CASCADE,
        related_name='bookings', verbose_name='کلاس'
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING, verbose_name='وضعیت')
    cancelled_at = models.DateTimeField(blank=True, null=True, verbose_name='تاریخ لغو')
    cancellation_reason = models.CharField(max_length=255, blank=True, verbose_name='دلیل لغو')
    notes = models.TextField(blank=True, verbose_name='یادداشت')

    class Meta:
        verbose_name = 'رزرو'
        verbose_name_plural = 'رزروها'
        ordering = ['-created_at']
        unique_together = ('student', 'class_session')

    def __str__(self):
        return f'{self.student.get_full_name()} - {self.class_session.title}'

    def clean(self):
        if self.pk is None and self.status == self.Status.PENDING:
            if self.class_session.is_full:
                raise ValidationError('ظرفیت این کلاس تکمیل است.')

    def get_absolute_url(self):
        return reverse('bookings:detail', kwargs={'pk': self.pk})

    def cancel(self, reason=''):
        from django.utils import timezone
        self.status = self.Status.CANCELLED
        self.cancelled_at = timezone.now()
        self.cancellation_reason = reason
        self.save()
