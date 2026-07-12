from django import forms
from django.contrib.auth import get_user_model

from .models import StudentProfile

User = get_user_model()


class StudentCreateForm(forms.ModelForm):
    """فرم ثبت هنرجوی جدید توسط مدیر (شامل اطلاعات کاربر + پروفایل)."""
    first_name = forms.CharField(label='نام', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='نام خانوادگی', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='ایمیل', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(
        label='شماره موبایل', max_length=11,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='رمز عبور اولیه',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = StudentProfile
        fields = ('level', 'birth_date', 'address', 'emergency_contact_name',
                  'emergency_contact_phone', 'medical_notes')
        widgets = {
            'level': forms.Select(attrs={'class': 'form-select'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'medical_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('این ایمیل قبلاً ثبت شده است.')
        return email

    def save(self, commit=True):
        user = User(
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            phone_number=self.cleaned_data['phone_number'],
            role=User.Role.STUDENT,
        )
        user.set_password(self.cleaned_data['password'])
        user.save()  # این خط به‌صورت خودکار (از طریق signal) یک StudentProfile خالی می‌سازد

        # به‌جای ساخت یک پروفایل جدید، همان پروفایلی که signal ساخته را می‌گیریم و تکمیل می‌کنیم
        profile = user.student_profile
        profile.level = self.cleaned_data['level']
        profile.birth_date = self.cleaned_data['birth_date']
        profile.address = self.cleaned_data['address']
        profile.emergency_contact_name = self.cleaned_data['emergency_contact_name']
        profile.emergency_contact_phone = self.cleaned_data['emergency_contact_phone']
        profile.medical_notes = self.cleaned_data['medical_notes']
        if commit:
            profile.save()
        return profile


class StudentUpdateForm(forms.ModelForm):
    """فرم ویرایش اطلاعات هنرجو توسط مدیر."""

    class Meta:
        model = StudentProfile
        fields = ('membership_status', 'level', 'birth_date', 'address',
                  'emergency_contact_name', 'emergency_contact_phone', 'medical_notes')
        widgets = {
            'membership_status': forms.Select(attrs={'class': 'form-select'}),
            'level': forms.Select(attrs={'class': 'form-select'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'medical_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }