from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View


class DashboardRedirectView(LoginRequiredMixin, View):
    """
    پس از ورود، کاربر بر اساس نقش خود (Admin/Coach/Student)
    به داشبورد اختصاصی خودش هدایت می‌شود.
    """

    def get(self, request):
        user = request.user
        if user.is_superuser or user.role == 'admin':
            return redirect('dashboard:admin_home')
        elif user.role == 'coach':
            return redirect('dashboard:coach_home')
        return redirect('dashboard:student_home')


from .admin_views import AdminHomeView  # noqa
from .coach_views import CoachHomeView  # noqa
from .student_views import StudentHomeView  # noqa

