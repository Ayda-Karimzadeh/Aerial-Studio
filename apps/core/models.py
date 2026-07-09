from django.db import models


class TimeStampedModel(models.Model):
    """
    مدل انتزاعی پایه که فیلدهای created_at و updated_at را
    به تمام مدل‌های ارث‌بر اضافه می‌کند.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    class Meta:
        abstract = True
        ordering = ['-created_at']


class SoftDeleteModel(models.Model):
    """
    مدل انتزاعی برای حذف نرم (Soft Delete) - رکورد واقعاً حذف نمی‌شود
    بلکه غیرفعال علامت‌گذاری می‌شود.
    """
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        abstract = True
