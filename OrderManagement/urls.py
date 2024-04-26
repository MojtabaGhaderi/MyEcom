
from django.urls import path
from . import views

urlpatterns = [
    path('pay/', views.OrderListView.as_view(), name='orders'),
    path('history/', views.OrderDetailView.as_view(), name='order_detail')
]
