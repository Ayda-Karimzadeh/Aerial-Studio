from django import forms
from django.contrib.auth import get_user_model

from .models import CoachProfile, WeeklySchedule

User = get_user_model()


class CoachCreateForm(forms.ModelForm):
    """فرم ثبت مربی جدید توسط مدیر."""
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
        model = CoachProfile
        fields = ('specialties', 'bio', 'years_of_experience', 'instagram')
        widgets = {
            'specialties': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'years_of_experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'instagram': forms.TextInput(attrs={'class': 'form-control'}),
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
            role=User.Role.COACH,
        )
        user.set_password(self.cleaned_data['password'])
        user.save()

        profile = super().save(commit=False)
        profile.user = user
        if commit:
            profile.save()
            self.save_m2m()
        return profile


class CoachUpdateForm(forms.ModelForm):
    """فرم ویرایش اطلاعات مربی."""

    class Meta:
        model = CoachProfile
        fields = ('specialties', 'bio', 'years_of_experience', 'instagram', 'is_active')
        widgets = {
            'specialties': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'years_of_experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'instagram': forms.TextInput(attrs={'class': 'form-control'}),
        }


class WeeklyScheduleForm(forms.ModelForm):
    """فرم افزودن برنامه هفتگی مربی."""

    class Meta:
        model = WeeklySchedule
        fields = ('weekday', 'start_time', 'end_time')
        widgets = {
            'weekday': forms.Select(attrs={'class': 'form-select'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }
