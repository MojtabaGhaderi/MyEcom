from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('category-create', views.CategoryCreateView.as_view(), name='category-create'),
    path('category-edit', views.CategoryEditView.as_view(), name='category-edit'),
]