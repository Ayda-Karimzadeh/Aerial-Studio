from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.PaymentListView.as_view(), name='list'),
    path('my-payments/', views.MyPaymentListView.as_view(), name='my_payments'),
    path('create/<int:booking_pk>/', views.PaymentCreateView.as_view(), name='create'),
    path('<int:pk>/', views.PaymentDetailView.as_view(), name='detail'),
    path('<int:pk>/mark-paid/', views.MarkPaymentPaidView.as_view(), name='mark_paid'),
    path('<int:pk>/refund/', views.RefundPaymentView.as_view(), name='refund'),
]
