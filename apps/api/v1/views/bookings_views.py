from rest_framework import viewsets, permissions

from apps.bookings.models import Booking
from apps.api.v1.serializers.bookings_serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """
    API رزروها - هر هنرجو فقط رزروهای خودش را می‌بیند،
    مدیر به همه رزروها دسترسی دارد.
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.role == 'admin':
            return Booking.objects.select_related('student', 'class_session').all()
        return Booking.objects.filter(student=user).select_related('class_session')

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
