from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView, FormView

from .forms import RegisterForm, LoginForm, ProfileUpdateForm, CustomPasswordChangeForm
from .models import User


class RegisterView(CreateView):
    """ثبت‌نام هنرجوی جدید در سایت."""
    model = User
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'ثبت‌نام با موفقیت انجام شد. اکنون می‌توانید وارد شوید.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'لطفاً خطاهای فرم را برطرف کنید.')
        return super().form_invalid(form)


class LoginView(FormView):
    """ورود کاربر با ایمیل و رمز عبور."""
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return reverse_lazy('dashboard:redirect')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f'خوش آمدید {user.get_full_name()}!')
            return super().form_valid(form)
        messages.error(self.request, 'ایمیل یا رمز عبور اشتباه است.')
        return self.form_invalid(form)


class LogoutView(View):
    """خروج کاربر از سیستم."""

    def get(self, request):
        logout(request)
        messages.info(request, 'با موفقیت خارج شدید.')
        return redirect('pages:home')


class ProfileView(LoginRequiredMixin, TemplateView):
    """نمایش پروفایل کاربر."""
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_obj'] = self.request.user
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """ویرایش اطلاعات پروفایل."""
    model = User
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'پروفایل با موفقیت به‌روزرسانی شد.')
        return super().form_valid(form)


class ChangePasswordView(LoginRequiredMixin, FormView):
    """تغییر رمز عبور کاربر."""
    form_class = CustomPasswordChangeForm
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('accounts:profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, 'رمز عبور با موفقیت تغییر یافت.')
        return super().form_valid(form)


class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
