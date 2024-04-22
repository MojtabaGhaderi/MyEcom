from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import AddProductToCartView, UserShoppingCardView, UserShoppingCartUpdate, EmptyUserShoppingCart, \
    InvoiceListView, InvoiceDetailView

urlpatterns = [

    path('add-product/', AddProductToCartView.as_view(), name='add-to-cart'),
    path('update/', UserShoppingCartUpdate.as_view(), name='cart-update'),
    path('empty/', EmptyUserShoppingCart.as_view(), name='empty-cart'),
    path('view/', UserShoppingCardView.as_view(), name='cart_view'),
    path('shop-history/', InvoiceListView.as_view(), name='invoice_list'),
    path('invoice/<int:pk>', InvoiceDetailView.as_view(), name='invoice-detail')
]

