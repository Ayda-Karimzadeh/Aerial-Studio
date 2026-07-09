from django import forms
from .models import Booking


class BookingCreateForm(forms.ModelForm):
    """فرم رزرو کلاس توسط هنرجو."""

    class Meta:
        model = Booking
        fields = ('notes',)
        widgets = {
            'notes': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 2,
                'placeholder': 'یادداشت اختیاری (مثلاً نیاز خاص یا توضیح)...'
            }),
        }


class BookingCancelForm(forms.ModelForm):
    """فرم لغو رزرو توسط هنرجو."""

    class Meta:
        model = Booking
        fields = ('cancellation_reason',)
        widgets = {
            'cancellation_reason': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 2,
                'placeholder': 'دلیل لغو رزرو...'
            }),
        }
