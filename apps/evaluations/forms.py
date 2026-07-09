from django import forms
from django.contrib.auth import get_user_model

from .models import Evaluation

User = get_user_model()


class EvaluationForm(forms.ModelForm):
    """فرم ثبت ارزیابی هنرجو توسط مربی."""

    class Meta:
        model = Evaluation
        fields = ('student', 'class_session', 'skill_level', 'score', 'description')
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'class_session': forms.Select(attrs={'class': 'form-select'}),
            'skill_level': forms.Select(attrs={'class': 'form-select'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, coach=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = User.objects.filter(role='student')
        if coach is not None:
            from apps.classes.models import ClassSession
            self.fields['class_session'].queryset = ClassSession.objects.filter(coach=coach)
