
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

import ShoppingCart
from PayManagement.models import InvoiceModel
from ShoppingCart.models import ShoppingCartModel


# def generate_invoice(request, shopping_cart_id):
#     shopping_cart = get_object_or_404(ShoppingCartModel, id=shopping_cart_id)
#
#     invoice = InvoiceModel.objects.create(user=shopping_cart.user)
#
#     for cart_item in shopping_cart.cartitmemodel_set.all():
#         invoice.invoice_products.add(cart_item.product, through_defaults={'quantity': cart_item.quantity})
#
#     invoice.amount = request.data['final_price']
#     invoice.save()
#     return invoice

class UserPayInfo(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        email = request.data.get('email')
        description = request.data.get('description')
        final_price = request.session.get('final_price')
        shopping_cart_id = request.session.get('shopping_cart_id')
        shopping_cart = ShoppingCart.objects.get(id=shopping_cart_id)
        data = {
            "Phone_number": phone_number,
            "Email": email,
            "Description": description,
            'Final_price': final_price,
            'shopping_cart': shopping_cart
        }
        return Response(data)

# def initiate_payment(request):
#     data = UserPayInfo()
#
#     final_price = request.session.get('final_price')
#     shopping_cart_id = request.session.get('shopping_cart_id')
#     shopping_cart = ShoppingCart.objects.get(id=shopping_cart_id)


# class PaymentView(APIView):
#
#     def get_invoice_number(self, shopping_cart_id):
#         invoice_number = generate_invoice(shopping_cart_id=shopping_cart_id)
#         return invoice_number


# class PaymentHistory(generics.ListAPIView):
#     queryset = PaymentModel.objects.all()
#     serializer_class = PaymentHistorySerializer

    # def get_queryset(self):
    #     user = self.request.user
    #     queryset = PaymentModel.objects.filter(invoice__user=user)
    #     return queryset



