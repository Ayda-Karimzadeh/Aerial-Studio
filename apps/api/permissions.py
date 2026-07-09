from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """فقط مدیر می‌تواند تغییر دهد؛ سایرین فقط خواندن."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and
                    (request.user.is_superuser or request.user.role == 'admin'))


class IsOwnerStudent(permissions.BasePermission):
    """فقط صاحب رزرو (هنرجو) اجازه دسترسی به رزرو خودش را دارد."""

    def has_object_permission(self, request, view, obj):
        return obj.student == request.user
