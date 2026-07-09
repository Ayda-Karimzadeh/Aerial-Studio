from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.api.v1.views.classes_views import ClassSessionViewSet, DisciplineViewSet
from apps.api.v1.views.bookings_views import BookingViewSet

router = DefaultRouter()
router.register('classes', ClassSessionViewSet, basename='class')
router.register('disciplines', DisciplineViewSet, basename='discipline')
router.register('bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
]
