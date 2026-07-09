from rest_framework import serializers

from apps.bookings.models import Booking


class BookingSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    class_title = serializers.CharField(source='class_session.title', read_only=True)

    class Meta:
        model = Booking
        fields = (
            'id', 'student', 'student_name', 'class_session', 'class_title',
            'status', 'notes', 'created_at',
        )
        read_only_fields = ('student', 'status', 'created_at')
