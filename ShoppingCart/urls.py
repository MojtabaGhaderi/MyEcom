from django.urls import path
from .views import AddProductToCartView

urlpatterns = [

    path('add-to-cart/', AddProductToCartView.as_view(), name='add-to-cart'),
]