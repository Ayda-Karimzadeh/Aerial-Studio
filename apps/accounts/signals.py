from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User


@receiver(post_save, sender=User)
def create_role_profile(sender, instance, created, **kwargs):
    """
    پس از ساخت کاربر جدید، بسته به نقش او، پروفایل مرتبط
    (StudentProfile یا CoachProfile) به‌صورت خودکار ساخته می‌شود.
    """
    if not created:
        return

    if instance.role == User.Role.STUDENT:
        from apps.students.models import StudentProfile
        StudentProfile.objects.get_or_create(user=instance)
    elif instance.role == User.Role.COACH:
        from apps.coaches.models import CoachProfile
        CoachProfile.objects.get_or_create(user=instance)
