
from django.urls import path
from . import views

urlpatterns = [

    path('pay/', views.PaymentView.as_view(), name='pay'),
    path('history/', views.PaymentHistory.as_view(), name='payment-history')
]