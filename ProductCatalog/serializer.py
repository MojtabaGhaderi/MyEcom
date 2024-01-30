from rest_framework import serializers
from .models import CategoryModel


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ['name']


class CategoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ['name']
        # read_only_fields = ['name'] /// changed this for edit_name view


class CategoryTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'
