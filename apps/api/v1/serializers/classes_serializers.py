from rest_framework import serializers

from apps.classes.models import ClassSession, Discipline


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ('id', 'name', 'description', 'icon')


class ClassSessionSerializer(serializers.ModelSerializer):
    discipline_name = serializers.CharField(source='discipline.get_name_display', read_only=True)
    coach_name = serializers.CharField(source='coach.get_full_name', read_only=True)
    remaining_capacity = serializers.IntegerField(read_only=True)
    is_full = serializers.BooleanField(read_only=True)

    class Meta:
        model = ClassSession
        fields = (
            'id', 'title', 'discipline', 'discipline_name', 'level', 'coach', 'coach_name',
            'capacity', 'equipment_count', 'price', 'session_date', 'start_time', 'end_time',
            'description', 'is_active', 'remaining_capacity', 'is_full',
        )
