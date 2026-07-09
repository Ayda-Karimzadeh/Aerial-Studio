from django.conf import settings
from django.db import models
from django.urls import reverse

from apps.core.models import TimeStampedModel


class StudentProfile(TimeStampedModel):
    """پروفایل تخصصی هنرجو، مرتبط با کاربر (User) به‌صورت OneToOne."""

    class MembershipStatus(models.TextChoices):
        ACTIVE = 'active', 'فعال'
        INACTIVE = 'inactive', 'غیرفعال'
        SUSPENDED = 'suspended', 'معلق'
        EXPIRED = 'expired', 'منقضی شده'

    class SkillLevel(models.TextChoices):
        BEGINNER = 'beginner', 'مبتدی'
        INTERMEDIATE = 'intermediate', 'متوسط'
        ADVANCED = 'advanced', 'پیشرفته'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='student_profile', verbose_name='کاربر'
    )
    membership_status = models.CharField(
        max_length=10, choices=MembershipStatus.choices,
        default=MembershipStatus.ACTIVE, verbose_name='وضعیت عضویت'
    )
    level = models.CharField(
        max_length=15, choices=SkillLevel.choices,
        default=SkillLevel.BEGINNER, verbose_name='سطح هنرجو'
    )
    birth_date = models.DateField(blank=True, null=True, verbose_name='تاریخ تولد')
    address = models.TextField(blank=True, verbose_name='آدرس')
    emergency_contact_name = models.CharField(max_length=100, blank=True, verbose_name='نام تماس اضطراری')
    emergency_contact_phone = models.CharField(max_length=11, blank=True, verbose_name='شماره تماس اضطراری')
    medical_notes = models.TextField(blank=True, verbose_name='یادداشت‌های پزشکی')
    joined_date = models.DateField(auto_now_add=True, verbose_name='تاریخ عضویت در باشگاه')

    class Meta:
        verbose_name = 'پروفایل هنرجو'
        verbose_name_plural = 'پروفایل‌های هنرجویان'
        ordering = ['-created_at']

    def __str__(self):
        return self.user.get_full_name()

    def get_absolute_url(self):
        return reverse('students:detail', kwargs={'pk': self.pk})

    @property
    def total_bookings(self):
        return self.user.bookings.count()

    @property
    def active_bookings_count(self):
        return self.user.bookings.filter(status='confirmed').count()
