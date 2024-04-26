
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from PaymentGateway.models import PaymentModel
from PaymentGateway.serializer import PaymentHistorySerializer
from ShoppingCart.models import InvoiceModel, ShoppingCartModel


def generate_invoice(request, shopping_cart_id):
    shopping_cart = get_object_or_404(ShoppingCartModel, id=shopping_cart_id)

    invoice = InvoiceModel.objects.create(user=shopping_cart.user)

    for cart_item in shopping_cart.cartitmemodel_set.all():
        invoice.invoice_products.add(cart_item.product, through_defaults={'quantity': cart_item.quantity})

    invoice.amount = request.data['final_price']
    invoice.save()
    return invoice.invoice_number


def initiate_payment(request):
    final_price = request.POST.get('final_price')
    payment_intent = PaymentModel.objects.create(
        amount=final_price,
        user=request.user,
        status='pending',

    )


class PaymentView(APIView):

    def get_invoice_number(self, shopping_cart_id):
        invoice_number = generate_invoice(shopping_cart_id=shopping_cart_id)
        return invoice_number

    def post(self, request, *args, **kwargs):
        payed = True
        shopping_cart_id = request.data['shopping_cart_id']
        invoice_number = self.get_invoice_number(shopping_cart_id=shopping_cart_id)
        try:
            invoice = InvoiceModel.objects.get(invoice_number=invoice_number)
            if payed:
                invoice.payment_status = True
            else:
                invoice.payment_status = False
            invoice.save()
            return Response("Payment processed successfully.")
        except InvoiceModel.DoesNotExist:
            return Response("Invoice not found.", status=status.HTTP_404_NOT_FOUND)


class PaymentHistory(generics.ListAPIView):
    queryset = PaymentModel.objects.all()
    serializer_class = PaymentHistorySerializer

    def get_queryset(self):
        user = self.request.user
        queryset = PaymentModel.objects.filter(invoice__user=user)
        return queryset



