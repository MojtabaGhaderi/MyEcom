from rest_framework import serializers
from .models import UserManageModel


# handles registration.//
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserManageModel
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = UserManageModel(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserManageModel
        fields = ['id', 'username', 'email', 'address', 'phone_number']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserManageModel
        fields = ['id', 'username', 'email', 'address', 'phone_number']

