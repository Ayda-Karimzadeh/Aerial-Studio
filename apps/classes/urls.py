from django.urls import path
from . import views

app_name = 'classes'

urlpatterns = [
    path('', views.ClassListView.as_view(), name='list'),
    path('manage/', views.ClassManageListView.as_view(), name='manage_list'),
    path('create/', views.ClassCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ClassDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ClassUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.ClassDeleteView.as_view(), name='delete'),
]
