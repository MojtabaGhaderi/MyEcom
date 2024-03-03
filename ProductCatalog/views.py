from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CategoryModel, ProductModel, ProductComment
from rest_framework import generics, viewsets, status
from .serializer import CategorySerializer, ProductAddEditSerializer, ProductUpdateSerializer, CommentSerializer


#  ///////////  Category related views  ///////////

class CategoryTestView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = CategoryModel.objects.all()


class CategoryCreateView(generics.CreateAPIView):
    serializer_class = CategorySerializer
    queryset = CategoryModel.objects.all()


class CategoryEditView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = CategoryModel.objects.all()

    def perform_destroy(self, instance):
        parents = instance.parent.all()
        children = CategoryModel.objects.filter(parent=instance)
        products = ProductModel.objects.filter(category=instance)

        for child in children:
            child.parent.set(parents)

        for product in products:
            product.category.set(parents)

        instance.delete()

#  /////  ^^^^^  ///////

# //////////    Product related views    //////////


class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductAddEditSerializer
    queryset = ProductModel.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        product_serializer = self.get_serializer(data=request.data)
        product_serializer.is_valid(raise_exception=True)
        self.perform_create(product_serializer)

        return Response(product_serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(status=204)


class ProductCommentDelete(generics.DestroyAPIView):  # admin related view
    queryset = ProductComment.objects.all()
    serializer_class = CommentSerializer


class ProductBatchUpdateView(APIView):
    serializer_class = ProductUpdateSerializer

    def put(self, request):
        serializer = self.serializer_class(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_batch_update(serializer)
        return Response({'message': 'Batch update was successful'})

    def perform_batch_update(self, serializer):
        for item in serializer.validated_data:
            product_id = item['id']
            product = ProductModel.objects.get(id=product_id)
            product.special_offer = item['special_offer']
            product.discount = item['discount']
            product.save()










