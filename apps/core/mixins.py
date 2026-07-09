from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class RoleRequiredMixin(UserPassesTestMixin):
    """
    Mixin عمومی برای محدود کردن دسترسی به Viewها بر اساس نقش کاربر.
    در ویوهای فرزند، allowed_roles باید تعریف شود، مثلاً:
    allowed_roles = ['admin', 'coach']
    """
    allowed_roles = []
    raise_exception = True

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return user.role in self.allowed_roles

    def handle_no_permission(self):
        raise PermissionDenied('شما اجازه دسترسی به این بخش را ندارید.')


class AdminRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['admin']


class CoachRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['coach']


class StudentRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['student']


class AdminOrCoachRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['admin', 'coach']
