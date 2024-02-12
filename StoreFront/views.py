from django.shortcuts import render
from rest_framework import generics

from ProductCatalog.models import ProductModel, CategoryModel
from .serializer import ProductsSerializer, ProductDetailSerializer


def filter_products(queryset, params):
    category = params.get('category')
    max_price = params.get('max_price')
    min_price = params.get('min_price')
    has_discount = params.get('has_discount')
    available = params.get('available')
    recently_added = params.get('recently_added')

    if category:
        queryset = queryset.filter(category__name=category)

    if max_price and min_price:
        queryset = queryset.filter(final_price__gte=min_price, final_price__lte=max_price)
    elif max_price:
        queryset = queryset.filter(final_price__lte=max_price)
    elif min_price:
        queryset = queryset.filter(final_price__gte=min_price)

    if has_discount:
        queryset = queryset.filter(discount__gt=0)

    if available is True:
        queryset = queryset.filter(available=True)

    if recently_added is True:
        queryset = queryset.filter(recently_added=True)

    return queryset


def order_products(queryset, params):
    sort_by = params.get('sort_by')

    if sort_by == 'name':
        queryset = queryset.order_by('name')
    elif sort_by == 'discount':
        queryset = queryset.order_by('discount')
    elif sort_by == 'price':
        queryset = queryset.order_by('price')
    elif sort_by == 'final_price':
        queryset = queryset.order_by('final_price')
    elif sort_by == 'likes':
        queryset = queryset.order_by('likes')
    elif sort_by == 'sold_counts':
        queryset = queryset.order_by('sold_count')

    # Add the `-` prefix for descending order
    if sort_by.startswith('-'):
        queryset = queryset.reverse()

    return queryset


# list of all the products or filtering them by category
class ProductListView(generics.ListAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        if 'filtering' in params:
            queryset = filter_products(queryset, params)
        if 'sort_by' in params:
            queryset = order_products(queryset, params)
        return queryset


class SpecialOfferListView(generics.ListAPIView):
    queryset = ProductModel.objects.filter(special_offer=True)
    serializer_class = ProductsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        if 'filtering' in params:
            queryset = filter_products(queryset, params)
        if 'sort_by' in params:
            queryset = order_products(queryset, params)
        return queryset


class LastProductsView(generics.ListAPIView):
    queryset = ProductModel.objects.filter(recently_added=True)
    serializer_class = ProductsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        if 'filtering' in params:
            queryset = filter_products(queryset, params)
        if 'sort_by' in params:
            queryset = order_products(queryset, params)
        return queryset


#  seeing a single product information
class ProductRetrieveView(generics.RetrieveAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductDetailSerializer
