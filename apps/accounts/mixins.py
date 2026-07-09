# Re-export از core برای سازگاری و راحتی import در اپ accounts
from apps.core.mixins import (
    RoleRequiredMixin,
    AdminRequiredMixin,
    CoachRequiredMixin,
    StudentRequiredMixin,
    AdminOrCoachRequiredMixin,
)

__all__ = [
    'RoleRequiredMixin',
    'AdminRequiredMixin',
    'CoachRequiredMixin',
    'StudentRequiredMixin',
    'AdminOrCoachRequiredMixin',
]
