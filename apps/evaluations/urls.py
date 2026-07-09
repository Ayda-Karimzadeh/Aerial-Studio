from django.urls import path
from . import views

app_name = 'evaluations'

urlpatterns = [
    path('create/', views.EvaluationCreateView.as_view(), name='create'),
    path('coach/', views.CoachEvaluationListView.as_view(), name='coach_list'),
    path('student/', views.StudentEvaluationListView.as_view(), name='student_list'),
    path('<int:pk>/', views.EvaluationDetailView.as_view(), name='detail'),
]
