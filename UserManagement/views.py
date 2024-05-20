from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, status
from rest_framework.views import APIView

from rest_framework.response import Response

from .models import UserManageModel
from core.permissions import IsAdminOrSelf
from .serializers import UserRegistrationSerializer, UserProfileSerializer


# //////////

# views for admins:


# class UserListView(generics.ListAPIView):
#     queryset = UserManageModel.objects.all()
#     serializer_class = UserSerializer


# /////////

# Views for users:

# // handles login. //
class LoginAPIView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({'detail': 'authentication was successfull.'})
        return Response({'detail': 'invalid'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request, format=None):
        logout(request)
        return Response({'detail': 'Successfully logged out.'})


class UserRegistrationView(generics.CreateAPIView):
    queryset = UserManageModel.objects.all()
    serializer_class = UserRegistrationSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = IsAdminOrSelf
    queryset = UserManageModel.objects.all()
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return self.queryset.filter(user=self.get_object())



