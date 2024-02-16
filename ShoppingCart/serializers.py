from rest_framework import serializers
from .models import ShoppingCartModel


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCartModel
        fields = '__all__'
