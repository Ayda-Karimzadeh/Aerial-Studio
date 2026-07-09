import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse

from apps.core.models import TimeStampedModel


class Payment(TimeStampedModel):
    """مدل پرداخت مرتبط با هر رزرو کلاس."""

    class Status(models.TextChoices):
        PENDING = 'pending', 'در انتظار پرداخت'
        PAID = 'paid', 'پرداخت شده'
        FAILED = 'failed', 'ناموفق'
        REFUNDED = 'refunded', 'بازگشت وجه'

    class Method(models.TextChoices):
        ONLINE = 'online', 'پرداخت آنلاین'
        CASH = 'cash', 'نقدی'
        CARD_TO_CARD = 'card_to_card', 'کارت به کارت'

    tracking_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='کد پیگیری')
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='payments', limit_choices_to={'role': 'student'}, verbose_name='هنرجو'
    )
    booking = models.OneToOneField(
        'bookings.Booking', on_delete=models.CASCADE,
        related_name='payment', verbose_name='رزرو'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='مبلغ (تومان)')
    method = models.CharField(max_length=15, choices=Method.choices, default=Method.ONLINE, verbose_name='روش پرداخت')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING, verbose_name='وضعیت')
    paid_at = models.DateTimeField(blank=True, null=True, verbose_name='تاریخ پرداخت')
    gateway_ref_id = models.CharField(max_length=100, blank=True, verbose_name='کد ارجاع درگاه')
    notes = models.TextField(blank=True, verbose_name='یادداشت')

    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت‌ها'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.tracking_code} - {self.get_status_display()}'

    def get_absolute_url(self):
        return reverse('payments:detail', kwargs={'pk': self.pk})

    def mark_as_paid(self, gateway_ref_id=''):
        from django.utils import timezone
        self.status = self.Status.PAID
        self.paid_at = timezone.now()
        self.gateway_ref_id = gateway_ref_id
        self.save()

    def mark_as_failed(self):
        self.status = self.Status.FAILED
        self.save()

    def refund(self):
        self.status = self.Status.REFUNDED
        self.save()
