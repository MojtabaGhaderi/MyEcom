from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'product', views.ProductView, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('category-create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('category-edit/<int:pk>/', views.CategoryEditView.as_view(), name='category-edit'),
    path('category-list/', views.CategoryTestView.as_view(), name='category-list-test'),
    path('comment-delete/<int:pk>/', views.ProductCommentDelete.as_view(), name='comment-delete'),


    path('discount-special-batch/', views.ProductBatchUpdateView.as_view(), name='product-discount-special'),

    path('user-list/', views.UserListView.as_view(), name='user-list'),
    path('user-retrieve/<int:pk>/', views.UserRetrieveView.as_view(), name='user-retrieve'),

    path('notification-create/', views.NotificationCreate.as_view(), name='notification-create'),
    path('notification-edit/', views.NotificationEdit.as_view(), name='notification-edit'),

]
