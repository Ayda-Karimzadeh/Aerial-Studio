from django.urls import path
from . import views

app_name = 'coaches'

urlpatterns = [
    path('', views.CoachListView.as_view(), name='list'),
    path('manage/', views.CoachManageListView.as_view(), name='manage_list'),
    path('create/', views.CoachCreateView.as_view(), name='create'),
    path('<int:pk>/', views.CoachDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.CoachUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.CoachDeleteView.as_view(), name='delete'),
    path('<int:pk>/schedule/add/', views.WeeklyScheduleCreateView.as_view(), name='schedule_add'),
]