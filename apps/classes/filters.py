import django_filters
from django import forms

from .models import ClassSession, Discipline


class ClassSessionFilter(django_filters.FilterSet):
    """فیلتر جستجوی کلاس‌ها بر اساس رشته، سطح، مربی و تاریخ."""

    discipline = django_filters.ModelChoiceFilter(
        queryset=Discipline.objects.all(), label='رشته',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    level = django_filters.ChoiceFilter(
        choices=ClassSession.Level.choices, label='سطح',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    session_date = django_filters.DateFilter(
        label='تاریخ',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    is_active = django_filters.BooleanFilter(
        label='وضعیت',
        widget=forms.Select(choices=[('', '---'), (True, 'فعال'), (False, 'غیرفعال')], attrs={'class': 'form-select'})
    )

    class Meta:
        model = ClassSession
        fields = ['discipline', 'level', 'session_date', 'is_active']
