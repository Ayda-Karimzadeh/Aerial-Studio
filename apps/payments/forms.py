from django import forms
from .models import Payment


class PaymentCreateForm(forms.ModelForm):
    """فرم ثبت پرداخت برای یک رزرو (توسط مدیر یا سیستم)."""

    class Meta:
        model = Payment
        fields = ('amount', 'method', 'status', 'notes')
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'method': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
