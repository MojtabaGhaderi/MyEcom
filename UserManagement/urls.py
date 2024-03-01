from django.urls import path, include
from . import views

urlpatterns = [
    path('list/', views.UserListView.as_view(), name='user-list'),
    path('retrieve/<int:pk>/', views.UserRetrieveView.as_view(), name='user-retrieve'),

    # path('login2/', views.UserLoginView.as_view(), name='login2'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),

]

