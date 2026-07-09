from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.urls import reverse

from apps.core.models import TimeStampedModel
from apps.core.validators import validate_phone_number
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """
    مدل کاربری سفارشی که پایه احراز هویت تمام نقش‌های سیستم
    (مدیر / مربی / هنرجو) است. ایمیل به‌جای نام کاربری استفاده می‌شود.
    """

    class Role(models.TextChoices):
        ADMIN = 'admin', 'مدیر'
        COACH = 'coach', 'مربی'
        STUDENT = 'student', 'هنرجو'

    email = models.EmailField(unique=True, verbose_name='ایمیل')
    first_name = models.CharField(max_length=50, verbose_name='نام')
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی')
    phone_number = models.CharField(
        max_length=11, blank=True, null=True,
        validators=[validate_phone_number], verbose_name='شماره موبایل'
    )
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT, verbose_name='نقش')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='تصویر پروفایل')
    is_staff = models.BooleanField(default=False, verbose_name='دسترسی ادمین')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ عضویت')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
        ordering = ['-date_joined']

    def __str__(self):
        return f'{self.get_full_name()} ({self.get_role_display()})'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()

    def get_short_name(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse('accounts:profile')

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN

    @property
    def is_coach_role(self):
        return self.role == self.Role.COACH

    @property
    def is_student_role(self):
        return self.role == self.Role.STUDENT
