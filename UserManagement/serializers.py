from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from .models import UserManageModel, AdminModel


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    class Meta:
        model = UserManageModel
        fields = ['username', 'password']

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if not user.is_active:
                    raise serializers.ValidationError('User account is not active!')
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError('Invalid username or password!')
        else:
            raise serializers.ValidationError('Both username and password are required!')


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

