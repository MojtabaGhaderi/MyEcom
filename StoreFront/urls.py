from django.urls import path, include
from . import views


urlpatterns = [

    path('', views.ProductListView.as_view(), name='home'),
    path('product/<int:pk>/', views.ProductRetrieveView.as_view(), name='single_product'),
    path('special-offer/', views.SpecialOfferListView.as_view(), name='special_offer'),
]