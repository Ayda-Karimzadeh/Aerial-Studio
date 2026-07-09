import json

from .services import get_monthly_stats, get_discipline_distribution


def get_revenue_chart_data():
    """داده آماده برای نمودار خطی درآمد ماهانه (Chart.js)."""
    monthly = get_monthly_stats()
    return json.dumps({
        'labels': [m['month'] for m in monthly],
        'revenue': [m['revenue'] for m in monthly],
        'new_students': [m['new_students'] for m in monthly],
    })


def get_discipline_chart_data():
    """داده آماده برای نمودار دایره‌ای توزیع رشته‌ها."""
    distribution = get_discipline_distribution()
    return json.dumps({
        'labels': [d['name'] for d in distribution],
        'counts': [d['class_count'] for d in distribution],
    })
