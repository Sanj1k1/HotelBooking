from django.urls import path
from .views import PaymentViewSet

payment_list = PaymentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

payment_detail = PaymentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns = [
    path('payments/', payment_list, name='payment-list'),
    path('payments/<int:pk>/', payment_detail, name='payment-detail'),
    path('payments/<int:pk>/process/', PaymentViewSet.as_view({'post': 'process_payment'}), name='payment-process'),
    path('payments/my-payments/', PaymentViewSet.as_view({'get': 'my_payments'}), name='my-payments'),
]