from django.conf import settings
from django.db import models
from django.urls import reverse

from apps.core.models import TimeStampedModel


class CoachProfile(TimeStampedModel):
    """پروفایل تخصصی مربی، مرتبط با کاربر (User) به‌صورت OneToOne."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='coach_profile', verbose_name='کاربر'
    )
    specialties = models.ManyToManyField(
        'classes.Discipline', related_name='coaches', blank=True, verbose_name='تخصص‌ها'
    )
    bio = models.TextField(blank=True, verbose_name='بیوگرافی')
    years_of_experience = models.PositiveSmallIntegerField(default=0, verbose_name='سابقه (سال)')
    instagram = models.CharField(max_length=100, blank=True, verbose_name='اینستاگرام')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'پروفایل مربی'
        verbose_name_plural = 'پروفایل‌های مربیان'
        ordering = ['-created_at']

    def __str__(self):
        return self.user.get_full_name()

    def get_absolute_url(self):
        return reverse('coaches:detail', kwargs={'pk': self.pk})

    @property
    def total_classes(self):
        return self.user.coached_classes.count()


class WeeklySchedule(TimeStampedModel):
    """برنامه هفتگی حضور مربی (روزها و ساعات کاری)."""

    class Weekday(models.IntegerChoices):
        SATURDAY = 0, 'شنبه'
        SUNDAY = 1, 'یکشنبه'
        MONDAY = 2, 'دوشنبه'
        TUESDAY = 3, 'سه‌شنبه'
        WEDNESDAY = 4, 'چهارشنبه'
        THURSDAY = 5, 'پنجشنبه'
        FRIDAY = 6, 'جمعه'

    coach = models.ForeignKey(
        CoachProfile, on_delete=models.CASCADE,
        related_name='weekly_schedules', verbose_name='مربی'
    )
    weekday = models.IntegerField(choices=Weekday.choices, verbose_name='روز هفته')
    start_time = models.TimeField(verbose_name='ساعت شروع')
    end_time = models.TimeField(verbose_name='ساعت پایان')

    class Meta:
        verbose_name = 'برنامه هفتگی'
        verbose_name_plural = 'برنامه‌های هفتگی'
        ordering = ['weekday', 'start_time']
        unique_together = ('coach', 'weekday', 'start_time')

    def __str__(self):
        return f'{self.coach} - {self.get_weekday_display()} ({self.start_time}-{self.end_time})'
