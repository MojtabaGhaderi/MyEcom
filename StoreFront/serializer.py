from rest_framework import serializers
from ProductCatalog.models import ProductModel, CategoryModel


class ProductsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductModel
        fields = ['image', 'name', 'price', 'available']
        read_only_fields = ['image', 'name', 'price', 'available']


class ProductDetailSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = ProductModel
        fields = '__all__'
        # read_only_fields = '__all__'

    def get_final_price(self, obj):
        if self.context.get('show_final_price'):
            return obj.final_price
        return None
