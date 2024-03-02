# from django.conf import settings
# import requests
# import json
#
# if settings.SANDBOX:
#     sandbox = 'sandbox'
# else:
#     sandbox = 'www'
#
# ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
# ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
# ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
#
# amount = 1000  # Rial / Required
# description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# phone = 'YOUR_PHONE_NUMBER'  # Optional
# CallbackURL = 'http://127.0.0.1:8080/verify/'
#
#
# def send_request(request):
#     data = {
#         "MerchantID": settings.MERCHANT,
#         "Amount": amount,
#         "Description": description,
#         "Phone": phone,
#         "CallbackURL": CallbackURL,
#     }
#     data = json.dumps(data)
#     headers = {'content-type': 'application/json', 'content-length': str(len(data))}
#     try:
#         response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
#         if response.status_code == 200:
#             response = response.json()
#             if response['Status'] == 100:
#                 return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
#                         'authority': response['Authority']}
#             else:
#                 return {'status': False, 'code': str(response['Status'])}
#         return response
#     except requests.exceptions.Timeout:
#         return {'status': False, 'code': 'timeout'}
#     except requests.exceptions.ConnectionError:
#         return {'status': False, 'code': 'connection error'}
#
#
# def verify(authority):
#     data = {
#         "MerchantID": settings.MERCHANT,
#         "Amount": amount,
#         "Authority": authority,
#     }
#     data = json.dumps(data)
#     headers = {'content-type': 'application/json', 'content-length': str(len(data))}
#     response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
#     if response.status_code == 200:
#         response = response.json()
#         if response['Status'] == 100:
#             return {'status': True, 'RefID': response['RefID']}
#         else:
#             return {'status': False, 'code': str(response['Status'])}
#     return response
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



