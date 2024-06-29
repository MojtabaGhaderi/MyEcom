from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from PayManagement.models import InvoiceModel
from UserManagement.models import UserManageModel
from Backstore.models import ProductModel
from .models import ShoppingCartModel, CartItemModel
from .serializers import ShoppingCartSerializer, ShoppingCartUpdateSerializer, InvoiceSerializer
from core.permissions import IsAdminOrSelf

import uuid


# // calculates the total price of a cart. //
def calculate_total_price(cart):
    products = cart.products.all()
    total_price = 0
    final_price = 0
    for product in products:
        obj = CartItemModel.objects.get(shopping_cart=cart, products=product)
        quantity = obj.quantity
        final_price += product.final_price * quantity
        total_price += product.price * quantity
    total_discount = total_price - final_price
    return total_price, total_discount, final_price


# // adding product to shopping cart. if shopping cart didn't exist, it will create one. //
class AddProductToCartView(APIView):

    def post(self, request):
        product_id = request.data.get('product_id')
        product = ProductModel.objects.get(id=product_id)
        quantity = int(request.data.get('quantity'))
        try:
            user = self.request.user

            # // for authenticated users. //
            if user.is_authenticated:
                shopping_cart, created = ShoppingCartModel.objects.get_or_create(user=user)

            # // for anonymous users. //
            else:

                # // first we check for an anonymous_user_id, in case the shopping cart is already there. //
                anonymous_user_id = request.session.get('anonymous_user_id')

                if not anonymous_user_id:
                    anonymous_user_id = str(uuid.uuid4())
                    request.session['anonymous_user_id'] = anonymous_user_id

                shopping_cart, created = ShoppingCartModel.objects.get_or_create(anonymous_user_id=anonymous_user_id)

        except UserManageModel.DoesNotExist:
            return Response('User not found.', status=status.HTTP_404_NOT_FOUND)

        if quantity > product.quantity:
            return Response('number of selected product is more than the available numbers.')
        if not product.available:
            return Response('product is not available now.')

        # shopping_cart = shopping_cart(0)
        print('shopping cart is ', shopping_cart)
        cart_item, created = CartItemModel.objects.get_or_create(
            shopping_cart=shopping_cart,
            products=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            if cart_item.quantity > product.quantity:
                return Response('number of selected product is more than the available numbers.')
            cart_item.save()

        serializer = ShoppingCartSerializer(shopping_cart)

        return Response(serializer.data, status=status.HTTP_200_OK)


# // viewing the shopping cart. //
class UserShoppingCardView(APIView):
    permission_classes = [IsAdminOrSelf]
    serializer_class = ShoppingCartSerializer

    def get_object(self):
        user = self.request.user

        if user.is_authenticated:
            shopping_cart = user.shopping_cart
        else:
            anonymous_user_id = self.request.session.get('anonymous_user_id')
            shopping_cart = ShoppingCartModel.objects.filter(anonymous_user_id=anonymous_user_id)

        return shopping_cart

    def get(self, request):
        shopping_cart = self.get_object()
        price = calculate_total_price(shopping_cart)
        total_price, total_discount, final_price = price
        serializer = self.serializer_class(shopping_cart, context={'total_price': total_price,
                                                                   'total_discount': total_discount,

                                                                   'final_price': final_price})
        request.session['final_price'] = str(final_price)
        request.session['shopping_cart_id'] = shopping_cart.id
        request.session.modified = True

        return Response(serializer.data)


# //users should be able to make change in their shopping cart. //
class UserShoppingCartUpdate(generics.UpdateAPIView):
    permission_classes = IsAdminOrSelf
    serializer_class = ShoppingCartUpdateSerializer
    queryset = ShoppingCartModel.objects.all()

    def get_object(self):
        user = self.request.user

        if user.is_authenticated:
            shopping_cart = user.shopping_cart
        else:
            anonymous_user_id = self.request.session.get('anonymous_user_id')
            shopping_cart = ShoppingCartModel.objects.filter(anonymous_user_id=anonymous_user_id)

        return shopping_cart

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        shopping_cart = self.get_object()
        quantities = serializer.validated_data.get('quantities', {})
        deleted_products = serializer.validated_data.get('deleted_products', [])

        for product_id, quantity in quantities.items():
            cart_item = CartItemModel.objects.get(shopping_cart=shopping_cart, products=product_id)

            if quantity > 0:

                if quantity > ProductModel.objects.get(id=product_id).numbers:
                    return Response('number of selected product is more than the available numbers.')
                else:
                    cart_item.quantity = quantity
                    cart_item.save()
            else:
                cart_item.delete()

        for product_id in deleted_products:
            cart_item = CartItemModel.objects.get(shopping_cart=shopping_cart, products=product_id)
            cart_item.delete()

        return Response(status=status.HTTP_200_OK)


# //users should be able to empty their shopping cart by one click. //
class EmptyUserShoppingCart(generics.DestroyAPIView):
    permission_classes = IsAdminOrSelf
    serializer_class = ShoppingCartSerializer
    queryset = ShoppingCartModel.objects.all()

    def get_object(self):
        user = self.request.user

        if user.is_authenticated:
            shopping_cart = user.shopping_cart
        else:
            anonymous_user_id = self.request.session.get('anonymous_user_id')
            shopping_cart = ShoppingCartModel.objects.filter(anonymous_user_id=anonymous_user_id)

        return shopping_cart

    def destroy(self, request, *args, **kwargs):
        shopping_cart = self.get_object()
        items = CartItemModel.objects.filter(shopping_cart=shopping_cart)
        for item in items:
            item.delete()
        return Response(status=status.HTTP_200_OK)


# // list of invoices for a user. //
class InvoiceListView(generics.ListAPIView):
    permission_classes = [IsAdminOrSelf]
    queryset = InvoiceModel.objects.all()
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            queryset = InvoiceModel.objects.filter(user=user)

        else:
            anonymous_user_id = self.request.session.get('anonymous_user_id')
            queryset = InvoiceModel.objects.filter(anonymous_user_id=anonymous_user_id)

        return queryset


# // viewing a certain invoice. //
class InvoiceDetailView(generics.RetrieveAPIView):
    permission_classes = IsAdminOrSelf
    # same as above here
    queryset = InvoiceModel.objects.all()
    serializer_class = InvoiceSerializer










