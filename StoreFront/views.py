from django.db.models import ExpressionWrapper, DecimalField, F, Case, When, Value
from django.shortcuts import render
from rest_framework import generics

from rest_framework.filters import SearchFilter

from Backstore.models import ProductModel, NotificationModel, ProductComment
from Backstore.serializer import CommentSerializer, NotificationSerializer
from .serializer import ProductsSerializer, ProductDetailSerializer


# ability to filter products based on different fields. //
# tested with product list
def filter_products(queryset, params):
    category = params.get('category')
    max_price = params.get('max_price')
    min_price = params.get('min_price')
    has_discount = params.get('has_discount')
    available = bool(params.get('available'))
    recently_added = bool(params.get('recently_added'))
    tags = params.get('tags')

    if category:
        queryset = queryset.filter(category__name=category)
    if tags:
        queryset = queryset.filter(tags__name=tags)
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


# ability to order products by different fields. //
# tested with product list
def order_products(queryset, params):
    sort_by = params.get('sort_by')
    revers_query = False
    if sort_by.startswith('-'):
        revers_query = True
        sort_by = sort_by[1:]
    if sort_by == 'name':
        queryset = queryset.order_by('name')
    elif sort_by == 'discount':
        queryset = queryset.order_by('discount')
    elif sort_by == 'price':
        queryset = queryset.order_by(F('price').asc(nulls_last=True))
    elif sort_by == 'final_price':
        queryset = queryset.annotate(
            last_price=ExpressionWrapper(
                Case(
                    When(price__isnull=False, then=F('price') - (F('price') * (F('discount') / 100))),
                    default=Value(None)
                ),
                output_field=DecimalField()
            )
        ).order_by(F('last_price').asc(nulls_last=True))
    elif sort_by == 'likes':
        queryset = queryset.order_by('likes')
    elif sort_by == 'sold_counts':
        queryset = queryset.order_by('sold_count')

    # Add the `-` prefix for descending order
    if revers_query:
        queryset = queryset.order_by(F('last_price').desc(nulls_last=True))
    return queryset


class NotificationsListView(generics.ListAPIView):
    queryset = NotificationModel.objects.all()
    serializer_class = NotificationSerializer


class NotificationDetailView(generics.RetrieveAPIView):
    queryset = NotificationModel.objects.all()
    serializer_class = NotificationSerializer


# // list of all the products or filtering them by category. //
class ProductListView(generics.ListAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductsSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        search_query = params.get('search')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
            return queryset
        if 'filtering' in params:
            queryset = filter_products(queryset, params)
        if 'sort_by' in params:
            queryset = order_products(queryset, params)
        return queryset


#  // seeing a single product information. //
class ProductRetrieveView(generics.RetrieveAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


# // retrieves comment of a product. //
class ProductCommentListView(generics.ListAPIView):
    queryset = ProductComment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        queryset = ProductComment.objects.filter(product_id=product_id)
        return queryset


# // a view to see Special offers. //
class SpecialOfferListView(generics.ListAPIView):
    queryset = ProductModel.objects.filter(special_offer=True)
    serializer_class = ProductsSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        search_query = params.get('search')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
            return queryset
        if 'filtering' in params:
            queryset = filter_products(queryset, params)
        if 'sort_by' in params:
            queryset = order_products(queryset, params)
        return queryset


# // a view to see last new products. //
class LastProductsView(generics.ListAPIView):
    queryset = ProductModel.objects.filter(recently_added=True)
    serializer_class = ProductsSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        search_query = params.get('search')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
            return queryset
        if 'filtering' in params:
            queryset = filter_products(queryset, params)
        if 'sort_by' in params:
            queryset = order_products(queryset, params)
        return queryset


