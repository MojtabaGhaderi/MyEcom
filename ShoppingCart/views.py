from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from UserManagement.models import UserManageModel
from ProductCatalog.models import ProductModel
from .models import ShoppingCartModel
from .serializers import ShoppingCartSerializer


class AddProductToCartView(APIView):
    def post(self, request):
        try:
            user_id = request.data.get('user_id')
            product_id = request.data.get('product_id')

            user = UserManageModel.objects.get(id=user_id)
            product = ProductModel.objects.get(id=product_id)

            product_number = int(request.data.get('product_number'))

            if product_number > product.numbers:
                return Response('number of selected product is more than the available numbers.')
            if not product.available:
                return Response('product is not available now.')

            shopping_cart = user.shopping_cart
            shopping_cart.products.add(product)
            shopping_cart.product_numer = product_number

            shopping_cart.save()
            serializer = ShoppingCartSerializer(shopping_cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (UserManageModel.DoesNotExist, ProductModel.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserShoppingCardView(generics.RetrieveUpdateAPIView):
    queryset = ShoppingCartModel.objects.all()
    serializer_class = ShoppingCartSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = ShoppingCartModel.objects.filter(user=user)
        return queryset

    def calculate_total_price(self):
        products = self.get_queryset()
        total_price = 0
        final_price = 0
        for product in products:
            final_price += product.final_price * product.product_number
            total_price += product.price * product.product_number
        total_discount = total_price - final_price
        return total_price, total_discount, final_price


class Payment(APIView):
    pass




