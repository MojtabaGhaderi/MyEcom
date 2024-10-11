from datetime import timedelta

from django.db import transaction
from rest_framework import serializers
from .models import CategoryModel, ProductModel, ProductImage, ProductComment, NotificationModel, DiscountCodeModel, \
    TagsModel


#  ///////////  Category related serializers  ///////////

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryModel
        fields = ['name', 'parent']


#  /////  ^^^^^  ///////

# //////////    Product related serializers    //////////

# /////////////////////////////////////////////////////////////////////////
class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = '__all__'

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        return super().create(validated_data)


class ProductAddEditSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    images = ImageSerializer(many=True, required=False, source='product.images')
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=TagsModel.objects.all(), required=False)

    class Meta:
        model = ProductModel
        fields = '__all__'

    def validate(self, attrs):
        return super().validate(attrs)

    def create_images(self, product, images_data):
        image_serializer = ImageSerializer(data=images_data, many=True)
        image_serializer.is_valid(raise_exception=True)
        image_serializer.save(product=product)

    def create(self, validated_data):


        images_data = self.context.get('request').FILES.getlist('images')

        category_data = validated_data.pop('category', None)
        tags = validated_data.pop('tags', [])

        product = ProductModel.objects.create(**validated_data)

        if category_data:
            product.category.set(category_data)

        if images_data:
            self.create_images(product, images_data)

        if tags:
            product.tags.set(tags)

        return product
# //////////////////////////////////////////////////////////////////////////


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = '__all__'


class ProductBatchUpdateItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    special_offer = serializers.BooleanField(required=False)
    available = serializers.BooleanField(required=False)
    immediate_delivery = serializers.BooleanField(required=False)
    discount = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    tags = serializers.ListField(child=serializers.IntegerField(), required=False)
    category = serializers.ListField(child=serializers.IntegerField(), required=False)

    def update(self, instance, validated_data):
        try:
            product = ProductModel.objects.get(pk=validated_data.get('id'))
            product.special_offer = validated_data.get('special_offer')
            product.discount = validated_data.get('discount')
            product.available = validated_data.get('available')
            product.immediate_delivery = validated_data.get('immediate_delivery')
            product.tags.set(validated_data.get('tags'))
            product.category.set(validated_data.get('category'))
            product.save()
            return product
        except (ProductModel.DoesNotExist, ValueError):
            return None


# class ProductBatchUpdateSerializer(serializers.Serializer):
#     def update(self, instances, validated_data, request):
#         valid_products = validated_data
#         invalid_data = []
#
#         for item in request.data:
#             if item not in validated_data:
#                 serializer = ProductBatchUpdateItemSerializer(data=item)
#                 invalid_data.append(
#                     {
#                         'data': item,
#                         'errors': serializer.errors
#                     }
#                 )
#         for serializer in valid_products:
#             serializer.save()
#
#         return {
#             'valid_data': [serializer.data for serializer in valid_products],
#             'invalid_data': invalid_data
#         }


# //////////    Discount Code related serializers    //////////


class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCodeModel
        fields = '__all__'
        read_only_fields = ['date_added', 'created_by', 'used']

    def validate(self, data):
        if data['percentage'] < 0:
            raise serializers.ValidationError('Percentage cannot be negative')
        if data['quantity'] < 0:
            raise serializers.ValidationError('Quantity cannot be negative')
        try:
            if data['time_period'] < timedelta(seconds=0):
                raise serializers.ValidationError('duration cannot be negative')
        except:
            pass

        return data
# keep in mind adding a custom field with validators

# //////////    Notifications related serializers    //////////

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = NotificationModel
        fields = '__all__'


