from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from PaymentGateway.models import PaymentModel
from UserManagement.models import UserManageModel
from ProductCatalog.models import ProductModel
from .models import ShoppingCartModel, CartItemModel, InvoiceModel
from .serializers import ShoppingCartSerializer, ShoppingCartUpdateSerializer, InvoiceSerializer
from core.permissions import IsAdminOrSelf


def calculate_total_price(cart):
    products = cart.products.all()
    print("products:", products)
    total_price = 0
    final_price = 0
    for product in products:
        obj = CartItemModel.objects.get(shopping_cart=cart, products=product)
        quantity = obj.quantity
        final_price += product.final_price * quantity
        total_price += product.price * quantity
        print("product:", product)
        print("total price:", total_price)
        print("final price:", final_price)
    total_discount = total_price - final_price
    print("total price:", total_price)
    print("total discount:", total_discount)
    print("final price:", final_price)
    return total_price, total_discount, final_price


class AddProductToCartView(APIView):
    # permission_classes = IsAdminOrSelf

    def post(self, request):
        try:
            # user_id = request.data.get('user_id')
            user = self.request.user
            try:
                shopping_cart = user.shopping_cart
                print("shopping cart:", shopping_cart)
                print("so now the cart should exist!")
            except:
                shopping_cart = ShoppingCartModel.objects.create(user=user)
            product_id = request.data.get('product_id')
            # user = UserManageModel.objects.get(id=user_id)
            product = ProductModel.objects.get(id=product_id)
            print("user:", user)
            print("product:", product)

            quantity = int(request.data.get('quantity'))
            print("quantity:", quantity)

            if quantity > product.numbers:
                return Response('number of selected product is more than the available numbers.')
            if not product.available:
                return Response('product is not available now.')

            cart_item, created = CartItemModel.objects.get_or_create(
                shopping_cart=shopping_cart,
                products=product,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                if cart_item.quantity > product.numbers:
                    return Response('number of selected product is more than the available numbers.')
                cart_item.save()
                print("cart item quantity:", cart_item.quantity)

            serializer = ShoppingCartSerializer(shopping_cart)
            print("serializer:", serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (UserManageModel.DoesNotExist, ProductModel.DoesNotExist):
            print("we are in except")
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserShoppingCardView(APIView):
    permission_classes = IsAdminOrSelf
    serializer_class = ShoppingCartSerializer

    def get_object(self):
        user = self.request.user
        shopping_cart = user.shopping_cart
        return shopping_cart

    def get(self, request):
        shopping_cart = self.get_object()
        price = calculate_total_price(shopping_cart)
        total_price, total_discount, final_price = price
        serializer = self.serializer_class(shopping_cart, context={'total_price': total_price,
                                                                   'total_discount': total_discount,
                                                                   'final_price': final_price})
        return Response(serializer.data)



class UserShoppingCartUpdate(generics.UpdateAPIView):
    permission_classes = IsAdminOrSelf
    serializer_class = ShoppingCartUpdateSerializer
    queryset = ShoppingCartModel.objects.all()

    def get_object(self):
        shopping_cart = self.request.user.shopping_cart
        return shopping_cart

    def update(self, request, *args, **kwargs):
        print("we are in update method")
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        shopping_cart = self.get_object()
        quantities = serializer.validated_data.get('quantities', {})
        print("quantities:", quantities)
        deleted_products = serializer.validated_data.get('deleted_products', [])
        print("deleted products:", deleted_products)

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
            print("we are trying to delete something")
            cart_item = CartItemModel.objects.get(shopping_cart=shopping_cart, products=product_id)
            cart_item.delete()

        return Response(status=status.HTTP_200_OK)


class EmptyUserShoppingCart(generics.DestroyAPIView):
    permission_classes = IsAdminOrSelf
    serializer_class = ShoppingCartSerializer
    queryset = ShoppingCartModel.objects.all()

    def get_object(self):
        shopping_cart = self.request.user.shopping_cart
        return shopping_cart

    def destroy(self, request, *args, **kwargs):
        shopping_cart = self.get_object()
        items = CartItemModel.objects.filter(shopping_cart=shopping_cart)
        for item in items:
            item.delete()
        return Response(status=status.HTTP_200_OK)


class InvoiceListView(generics.ListAPIView):
    permission_classes = IsAdminOrSelf
    queryset = InvoiceModel.objects.all()
    serializer_class = InvoiceSerializer
# permission for being admin. we want to add a permission so admins can come here too. I think I must add an if
    # statement in def get_queryset
    def get_queryset(self):
        user = self.request.user
        queryset = InvoiceModel.objects.filter(user=user)
        return queryset


class InvoiceDetailView(generics.RetrieveAPIView):
    permission_classes = IsAdminOrSelf
    # same as above here
    queryset = InvoiceModel.objects.all()
    serializer_class = InvoiceSerializer










