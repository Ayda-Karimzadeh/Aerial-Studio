from django.db import models

from apps.core.models import TimeStampedModel


class GalleryImage(TimeStampedModel):
    """تصاویر گالری باشگاه که در صفحه Gallery نمایش داده می‌شوند."""
    title = models.CharField(max_length=100, blank=True, verbose_name='عنوان')
    image = models.ImageField(upload_to='gallery/', verbose_name='تصویر')
    discipline = models.ForeignKey(
        'classes.Discipline', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='gallery_images', verbose_name='رشته مرتبط'
    )
    is_featured = models.BooleanField(default=False, verbose_name='ویژه')

    class Meta:
        verbose_name = 'تصویر گالری'
        verbose_name_plural = 'گالری تصاویر'
        ordering = ['-created_at']

    def __str__(self):
        return self.title or f'تصویر گالری #{self.pk}'


class Testimonial(TimeStampedModel):
    """نظرات و بازخورد هنرجویان که در Landing Page نمایش داده می‌شود."""
    student_name = models.CharField(max_length=100, verbose_name='نام هنرجو')
    avatar = models.ImageField(upload_to='testimonials/', blank=True, null=True, verbose_name='تصویر')
    content = models.TextField(verbose_name='متن نظر')
    rating = models.PositiveSmallIntegerField(default=5, verbose_name='امتیاز (از ۵)')
    is_published = models.BooleanField(default=True, verbose_name='منتشر شده')

    class Meta:
        verbose_name = 'نظر هنرجو'
        verbose_name_plural = 'نظرات هنرجویان'
        ordering = ['-created_at']

    def __str__(self):
        return self.student_name


class ContactMessage(TimeStampedModel):
    """پیام‌های ارسالی از فرم تماس با ما."""
    full_name = models.CharField(max_length=100, verbose_name='نام کامل')
    email = models.EmailField(verbose_name='ایمیل')
    phone_number = models.CharField(max_length=11, blank=True, verbose_name='شماره تماس')
    subject = models.CharField(max_length=150, verbose_name='موضوع')
    message = models.TextField(verbose_name='پیام')
    is_read = models.BooleanField(default=False, verbose_name='خوانده شده')

    class Meta:
        verbose_name = 'پیام تماس'
        verbose_name_plural = 'پیام‌های تماس'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.full_name} - {self.subject}'
