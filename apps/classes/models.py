from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from apps.core.models import TimeStampedModel


class Discipline(TimeStampedModel):
    """رشته‌های تخصصی ورزش هوایی (Silk, Hoop, Sling, Stretch, Flexibility)."""

    class DisciplineType(models.TextChoices):
        SILK = 'silk', 'سیلک (پارچه هوایی)'
        HOOP = 'hoop', 'هوپ (حلقه هوایی)'
        SLING = 'sling', 'اسلینگ'
        STRETCH = 'stretch', 'استرچ'
        FLEXIBILITY = 'flexibility', 'انعطاف‌پذیری'

    name = models.CharField(max_length=20, choices=DisciplineType.choices, unique=True, verbose_name='نام رشته')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    icon = models.CharField(max_length=50, blank=True, help_text='کلاس آیکون Font Awesome', verbose_name='آیکون')
    cover_image = models.ImageField(upload_to='disciplines/', blank=True, null=True, verbose_name='تصویر کاور')

    class Meta:
        verbose_name = 'رشته'
        verbose_name_plural = 'رشته‌ها'
        ordering = ['name']

    def __str__(self):
        return self.get_name_display()


class ClassSession(TimeStampedModel):
    """مدل اصلی کلاس‌های باشگاه."""

    class Level(models.TextChoices):
        BEGINNER = 'beginner', 'مبتدی'
        INTERMEDIATE = 'intermediate', 'متوسط'
        ADVANCED = 'advanced', 'پیشرفته'

    title = models.CharField(max_length=150, verbose_name='نام کلاس')
    discipline = models.ForeignKey(
        Discipline, on_delete=models.PROTECT, related_name='class_sessions', verbose_name='رشته'
    )
    level = models.CharField(max_length=15, choices=Level.choices, verbose_name='سطح')
    coach = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        related_name='coached_classes', limit_choices_to={'role': 'coach'}, verbose_name='مربی'
    )
    capacity = models.PositiveSmallIntegerField(verbose_name='ظرفیت')
    equipment_count = models.PositiveSmallIntegerField(default=0, verbose_name='تعداد تجهیزات')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='قیمت (تومان)')
    session_date = models.DateField(verbose_name='تاریخ برگزاری')
    start_time = models.TimeField(verbose_name='ساعت شروع')
    end_time = models.TimeField(verbose_name='ساعت پایان')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    cover_image = models.ImageField(upload_to='classes/', blank=True, null=True, verbose_name='تصویر کلاس')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'کلاس'
        verbose_name_plural = 'کلاس‌ها'
        ordering = ['session_date', 'start_time']

    def __str__(self):
        return f'{self.title} - {self.session_date}'

    def clean(self):
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError('ساعت پایان باید بعد از ساعت شروع باشد.')

    def get_absolute_url(self):
        return reverse('classes:detail', kwargs={'pk': self.pk})

    @property
    def booked_count(self):
        return self.bookings.filter(status__in=['confirmed', 'pending']).count()

    @property
    def remaining_capacity(self):
        return max(self.capacity - self.booked_count, 0)

    @property
    def is_full(self):
        return self.remaining_capacity <= 0

    @property
    def fill_percentage(self):
        if self.capacity == 0:
            return 0
        return round((self.booked_count / self.capacity) * 100)
