from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'product', views.ProductView, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('product-create/', views.ProductView.as_view({'post': 'create'}), name='product-create'),
    path('product-update/<slug:slug>', views.ProductView.as_view({'put': 'update', 'patch': 'partial_update'}),
         name='product-update'),
    path('product-delete/<slug:slug>', views.ProductView.as_view({'delete': 'destroy'}), name='product-delete'),
    path('comment-delete/<int:pk>/', views.ProductCommentDelete.as_view(), name='comment-delete'),

    path('discount-special-batch/', views.ProductBatchUpdateView.as_view(), name='product-discount-special'),

    path('category-create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('category-edit/<int:pk>/', views.CategoryEditView.as_view(), name='category-edit'),
    path('category-list/', views.CategoryTestView.as_view(), name='category-list-test'),

    path('user-list/', views.UserListView.as_view(), name='user-list'),
    path('user-retrieve/<int:pk>/', views.UserRetrieveView.as_view(), name='user-retrieve'),

    path('discount-code-create/', views.DiscountCodeCreate.as_view(), name='discount-code-create'),
    path('discount-code-update/<int:pk>', views.DiscountCodeUpdate.as_view(), name='discount-code-update'),


    path('notification-create/', views.NotificationCreate.as_view(), name='notification-create'),
    path('notification-edit/<int:pk>', views.NotificationEdit.as_view(), name='notification-edit'),

]
# for url in router.get_urls():
#     print(url.name)