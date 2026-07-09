from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse

from apps.core.models import TimeStampedModel


class Evaluation(TimeStampedModel):
    """ارزیابی مربی از پیشرفت هنرجو - سوابق کامل نگهداری می‌شوند."""

    class SkillLevel(models.TextChoices):
        BEGINNER = 'beginner', 'مبتدی'
        INTERMEDIATE = 'intermediate', 'متوسط'
        ADVANCED = 'advanced', 'پیشرفته'

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='evaluations', limit_choices_to={'role': 'student'}, verbose_name='هنرجو'
    )
    coach = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='given_evaluations', limit_choices_to={'role': 'coach'}, verbose_name='مربی'
    )
    class_session = models.ForeignKey(
        'classes.ClassSession', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='evaluations', verbose_name='کلاس مرتبط'
    )
    skill_level = models.CharField(max_length=15, choices=SkillLevel.choices, verbose_name='سطح مهارت')
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)], verbose_name='امتیاز (از ۱۰)'
    )
    description = models.TextField(verbose_name='توضیحات ارزیابی')

    class Meta:
        verbose_name = 'ارزیابی'
        verbose_name_plural = 'ارزیابی‌ها'
        ordering = ['-created_at']

    def __str__(self):
        return f'ارزیابی {self.student.get_full_name()} توسط {self.coach.get_full_name()}'

    def get_absolute_url(self):
        return reverse('evaluations:detail', kwargs={'pk': self.pk})
