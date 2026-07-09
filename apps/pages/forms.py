from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """فرم تماس با ما."""

    class Meta:
        model = ContactMessage
        fields = ('full_name', 'email', 'phone_number', 'subject', 'message')
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کامل'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '09xxxxxxxxx'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'موضوع پیام'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'متن پیام...'}),
        }
