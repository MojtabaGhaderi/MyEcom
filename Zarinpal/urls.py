# Github.com/Rasooll
from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.send_request, name='request'),
    path('verify/', views.verify, name='verify'),
    path('pai/', views.PaymentView.as_view(), name='paying'),
    path('middlepay/', views.MiddlePayView.as_view(), name='middle'),
]
