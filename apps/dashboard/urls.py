from django.urls import path

from .views import DashboardRedirectView, AdminHomeView, CoachHomeView, StudentHomeView

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardRedirectView.as_view(), name='redirect'),
    path('admin/', AdminHomeView.as_view(), name='admin_home'),
    path('coach/', CoachHomeView.as_view(), name='coach_home'),
    path('student/', StudentHomeView.as_view(), name='student_home'),
]
