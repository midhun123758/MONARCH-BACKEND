from django.urls import path
from .views import OrderView, VerifyPaymentView, OrderHistoryView

urlpatterns = [
    path('orders/', OrderView.as_view(), name='orders'),
    path('verify-payment/', VerifyPaymentView.as_view(), name='verify-payment'),
    path('order-history/', OrderHistoryView.as_view(), name='order-history'),
]
