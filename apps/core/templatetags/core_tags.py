from django import template

register = template.Library()


@register.filter(name='persian_currency')
def persian_currency(value):
    """نمایش عدد به صورت پول با جداکننده هزارگان و پسوند تومان."""
    try:
        return f"{int(value):,} تومان".replace(',', '،')
    except (ValueError, TypeError):
        return value


@register.filter(name='badge_color')
def badge_color(status):
    """رنگ Badge بوت‌استرپ متناسب با وضعیت (برای رزرو/پرداخت)."""
    mapping = {
        'pending': 'warning',
        'paid': 'success',
        'failed': 'danger',
        'refunded': 'secondary',
        'confirmed': 'success',
        'cancelled': 'danger',
        'active': 'success',
        'inactive': 'secondary',
    }
    return mapping.get(str(status).lower(), 'primary')


@register.simple_tag
def percentage(part, total):
    """محاسبه درصد پر شدن ظرفیت کلاس‌ها."""
    try:
        return round((part / total) * 100)
    except (ZeroDivisionError, TypeError):
        return 0
