from django.urls import path, include
from . import views

urlpatterns = [
    path('list/', views.UserListView.as_view(), name='user-list'),
    path('retrieve/<int:pk>/', views.UserRetrieveView.as_view(), name='user-retrieve'),

    path('login/', views.UserLoginView.as_view(), name='login'),
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),

]
