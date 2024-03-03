from rest_framework import serializers
from .models import CategoryModel, ProductModel, ProductImage, ProductComment


#  ///////////  Category related serializers  ///////////

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ['name', 'parent']


#  /////  ^^^^^  ///////

# //////////    Product related serializers    //////////


class ImageSerializer(serializers.ModelSerializer):
    model = ProductImage

    class Meta:
        fields = ['image']


class ProductAddEditSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, required=False)

    class Meta:
        model = ProductModel
        fields = '__all__'

    def create(self, validated_data):
        images_data = validated_data.pop('images', None)
        category_data = validated_data.pop('category', None)
        product = ProductModel.objects.create(**validated_data)

        if category_data:
            product.category.set(category_data)

        if images_data:
            for image_data in images_data:
                ProductImage.objects.create(product=product, **image_data)
        return product


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = '__all__'



class ProductUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ProductModel
        fields = ['id', 'special_offer', 'discount']

