from django.shortcuts import render
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.response import Response

from .models import UserManageModel
from .serializers import UserSerializer, UserRegistrationSerializer, UserProfileSerializer, UserLoginSerializer


# //////////

# views for admins:


class UserListView(generics.ListAPIView):
    queryset = UserManageModel.objects.all()
    serializer_class = UserSerializer


class UserRetrieveView(generics.RetrieveUpdateAPIView):
    queryset = UserManageModel.objects.all()
    serializer_class = UserSerializer

# /////////

# Views for users:


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        })


class UserRegistrationView(generics.CreateAPIView):
    queryset = UserManageModel.objects.all()
    serializer_class = UserRegistrationSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = UserManageModel.objects.all()
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


