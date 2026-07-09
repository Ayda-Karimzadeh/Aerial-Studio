from rest_framework import viewsets

from apps.classes.models import ClassSession, Discipline
from apps.api.permissions import IsAdminOrReadOnly
from apps.api.v1.serializers.classes_serializers import ClassSessionSerializer, DisciplineSerializer


class DisciplineViewSet(viewsets.ModelViewSet):
    """API رشته‌های تخصصی."""
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer
    permission_classes = [IsAdminOrReadOnly]


class ClassSessionViewSet(viewsets.ModelViewSet):
    """API کلاس‌ها با امکان فیلتر بر اساس رشته و سطح."""
    queryset = ClassSession.objects.select_related('discipline', 'coach').all()
    serializer_class = ClassSessionSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['discipline', 'level', 'is_active']
