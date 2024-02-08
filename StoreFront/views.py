from django.shortcuts import render
from rest_framework import generics

from ProductCatalog.models import ProductModel, CategoryModel
from .serializer import ProductsSerializer, ProductDetailSerializer


# list of all the products or filtering them by category
class ProductListView(generics.ListAPIView):
    model = ProductModel.objects.all()
    serializer_class = ProductsSerializer

    def get_queryset(self):
        category = self.request.query_params.get('category')

        if category:
            queryset = ProductModel.objects.filter(category=category)
        else:
            queryset = ProductModel.objects.all()

        return queryset


#  seeing a single product information
class ProductRetrieveView(generics.RetrieveAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductDetailSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        print("we are in def get_serializer")
        if self.get_object().discount:
            print("object", self.get_object())
            print("discount:", self.get_object().discount)
            kwargs['context']['show_final_price'] = True

        return self.serializer_class(*args, **kwargs)

