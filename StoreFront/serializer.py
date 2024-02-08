from rest_framework import serializers
from ProductCatalog.models import ProductModel, CategoryModel


class ProductsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductModel
        fields = ['image', 'name', 'price', 'available']
        read_only_fields = ['image', 'name', 'price', 'available']


class ProductDetailSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField()
    print("we are in product detailserializer")

    class Meta:
        model = ProductModel
        fields = '__all__'
        # read_only_fields = '__all__'
        print("we are in meta of product detailserializer")

    def get_final_price(self, obj):
        print("we are in serializer final_price")
        if self.context.get('show_final_price'):
            print("show final price is true")
            return obj.final_price
        return None
