from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('category-create', views.CategoryCreateView.as_view(), name='category-create'),
    path('category-move/<int:pk>/', views.CategoryMoveView.as_view(), name='category-move'),
    path('category-edit/<int:pk>/', views.CategoryEditNameView.as_view(), name='category-edit'),
    path('category-list', views.CategoryTestView.as_view(), name='category-llist-test'),
]