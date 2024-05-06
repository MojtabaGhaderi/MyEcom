from rest_framework import serializers

from PayManagement.models import InvoiceModel
from .models import ShoppingCartModel


class ShoppingCartSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(max_digits=13, decimal_places=3, required=False)
    total_discount = serializers.DecimalField(max_digits=13, decimal_places=3, required=False)
    final_price = serializers.DecimalField(max_digits=13, decimal_places=3, required=False)

    class Meta:
        model = ShoppingCartModel
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['total_price'] = self.context.get('total_price')
        representation['total_discount'] = self.context.get('total_discount')
        representation['final_price'] = self.context.get('final_price')
        return representation


class ShoppingCartUpdateSerializer(serializers.Serializer):
    quantities = serializers.DictField(child=serializers.IntegerField(min_value=0), required=False)
    deleted_products = serializers.ListField(child=serializers.IntegerField(min_value=1), required=False)


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceModel
        fields = '__all__'
