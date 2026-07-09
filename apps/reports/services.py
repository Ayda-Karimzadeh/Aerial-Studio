from datetime import timedelta

from django.db.models import Count, Sum, Q
from django.utils import timezone

from apps.accounts.models import User
from apps.bookings.models import Booking
from apps.classes.models import ClassSession, Discipline
from apps.payments.models import Payment


def get_dashboard_stats():
    """آمار کلی برای داشبورد مدیر."""
    total_students = User.objects.filter(role=User.Role.STUDENT).count()
    total_coaches = User.objects.filter(role=User.Role.COACH).count()
    total_classes = ClassSession.objects.count()
    total_revenue = Payment.objects.filter(status=Payment.Status.PAID).aggregate(
        total=Sum('amount')
    )['total'] or 0

    return {
        'total_students': total_students,
        'total_coaches': total_coaches,
        'total_classes': total_classes,
        'total_revenue': total_revenue,
    }


def get_popular_discipline():
    """محبوب‌ترین رشته بر اساس تعداد رزروهای موفق."""
    return (
        Discipline.objects.annotate(
            booking_count=Count(
                'class_sessions__bookings',
                filter=Q(class_sessions__bookings__status__in=['confirmed', 'completed'])
            )
        ).order_by('-booking_count').first()
    )


def get_full_and_empty_classes():
    """کلاس‌های پر شده و خالی."""
    classes = ClassSession.objects.filter(is_active=True).annotate(
        booked_total=Count('bookings', filter=Q(bookings__status__in=['confirmed', 'pending']))
    )
    full_classes = [c for c in classes if c.booked_total >= c.capacity]
    empty_classes = [c for c in classes if c.booked_total == 0]
    return full_classes, empty_classes


def get_monthly_stats(months=6):
    """آمار ماهانه ثبت‌نام هنرجویان و درآمد برای نمودارها (چند ماه اخیر)."""
    today = timezone.now()
    data = []
    for i in range(months - 1, -1, -1):
        month_start = (today.replace(day=1) - timedelta(days=1)).replace(day=1) if i > 0 else today.replace(day=1)
        # ساده‌سازی: محاسبه بازه بر اساس ماه شمسی/میلادی جاری منهای i ماه
        target_month = today.month - i
        target_year = today.year
        while target_month <= 0:
            target_month += 12
            target_year -= 1

        revenue = Payment.objects.filter(
            status=Payment.Status.PAID,
            paid_at__year=target_year,
            paid_at__month=target_month
        ).aggregate(total=Sum('amount'))['total'] or 0

        new_students = User.objects.filter(
            role=User.Role.STUDENT,
            date_joined__year=target_year,
            date_joined__month=target_month
        ).count()

        data.append({
            'month': f'{target_year}/{target_month:02d}',
            'revenue': float(revenue),
            'new_students': new_students,
        })
    return data


def get_discipline_distribution():
    """توزیع تعداد کلاس‌ها بر اساس رشته (برای نمودار دایره‌ای)."""
    return list(
        Discipline.objects.annotate(class_count=Count('class_sessions')).values('name', 'class_count')
    )
