from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.ReportsView.as_view(), name='dashboard'),
]
