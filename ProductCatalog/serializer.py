from rest_framework import serializers
from .models import CategoryModel


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = 'name'


class CategoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ['name']
