from rest_framework import serializers
from Backstore.models import ProductModel, CategoryModel


class LastPriceField(serializers.Field):
    def get_attribute(self, instance):
        return instance.final_price

    def to_representation(self, value):
        return value


# // this one is for more than one product. //
class ProductsSerializer(serializers.ModelSerializer):
    last_price = LastPriceField()
    # last_price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = ProductModel
        fields = ['image', 'name', 'price', 'available', 'last_price']
        read_only_fields = ['image', 'name', 'price', 'available']


# // this one is for just one product. //
class ProductDetailSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = ProductModel
        fields = '__all__'

    def get_final_price(self, obj):
        return obj.final_price

