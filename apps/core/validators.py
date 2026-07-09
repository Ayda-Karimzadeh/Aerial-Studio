import re
from django.core.exceptions import ValidationError


def validate_phone_number(value):
    """اعتبارسنجی شماره تلفن ایرانی (موبایل)."""
    pattern = r'^09\d{9}$'
    if not re.match(pattern, value):
        raise ValidationError('شماره موبایل باید با 09 شروع شده و ۱۱ رقم باشد.')


def validate_image_size(image):
    """محدود کردن حجم تصویر آپلودی به حداکثر ۵ مگابایت."""
    max_size_mb = 5
    if image.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'حجم تصویر نباید بیشتر از {max_size_mb} مگابایت باشد.')
