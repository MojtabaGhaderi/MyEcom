from django.shortcuts import render
from rest_framework.response import Response

from .models import CategoryModel, ProductModel
from rest_framework import generics, viewsets, status
from .serializer import CategorySerializer, ProductAddEditSerializer


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
        print('in the list function')
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










