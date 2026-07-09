import django_filters
from django import forms

from .models import StudentProfile


class StudentFilter(django_filters.FilterSet):
    """فیلتر جستجو و فیلتر لیست هنرجویان."""

    search = django_filters.CharFilter(
        method='filter_search', label='جستجو',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام، ایمیل یا تلفن...'})
    )
    membership_status = django_filters.ChoiceFilter(
        choices=StudentProfile.MembershipStatus.choices, label='وضعیت عضویت',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    level = django_filters.ChoiceFilter(
        choices=StudentProfile.SkillLevel.choices, label='سطح',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = StudentProfile
        fields = ['search', 'membership_status', 'level']

    def filter_search(self, queryset, name, value):
        from django.db.models import Q
        return queryset.filter(
            Q(user__first_name__icontains=value) |
            Q(user__last_name__icontains=value) |
            Q(user__email__icontains=value) |
            Q(user__phone_number__icontains=value)
        )
