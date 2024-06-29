from django.urls import path, include
from . import views


urlpatterns = [

    path('', views.ProductListView.as_view(), name='home'),
    path('product/<slug:slug>/', views.ProductRetrieveView.as_view(), name='product'),
    path('special-offer/', views.SpecialOfferListView.as_view(), name='special_offer'),
    path('last-products/', views.LastProductsView.as_view(), name='recent-products'),
    path('product/<int:product_id>/comments', views.ProductCommentListView.as_view(), name='product_comments'),

    path('notification/', views.NotificationsListView.as_view(), name='notifications'),
    path('notification/<int:pk>', views.NotificationDetailView.as_view(), name='notification-detail'),

]