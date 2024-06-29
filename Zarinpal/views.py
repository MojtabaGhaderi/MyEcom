import urllib
from urllib.parse import quote

from django.conf import settings
import requests
import json

from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import ShoppingCart
from Backstore.models import DiscountCodeModel
from Backstore.serializer import DiscountCodeSerializer
from PayManagement.models import InvoiceModel
from ShoppingCart.models import ShoppingCartModel
from django.urls import reverse
#

# ? sandbox merchant
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

CallbackURL = 'http://127.0.0.1:8000/pay/verify/'


def send_request(request):
    print("we have arrived in send_request view")
    data = request.session.get('data')
    print("data in 13 is:", data)
    data.update({"MerchantID": settings.MERCHANT, "CallbackURL": CallbackURL})
    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    print("data is:", data)
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
        # here we send the data to zarinpal endpoint

        print("we are at 8")
        if response.status_code == 200:
            print("we are in 1")
            response_data = response.json()
            if response_data['Status'] == 100:
                print("we are in 2")

                print("response sata is:", response_data)
                return JsonResponse({'status': True, 'url': ZP_API_STARTPAY + str(response_data['Authority']),
                                     'authority': response_data['Authority']})
            else:
                print("we are in 3")

                return JsonResponse({'status': False, 'code': str(response_data['Status'])})
        else:
            print("we are in 4")
            print("Response status code:", response.status_code)
            print("Response content:", response.content)

            return JsonResponse({'status': False, 'code': 'request_failed', 'message': 'API request failed'},
                                status=response.status_code)

    except requests.exceptions.Timeout:
        print("we are in 5")

        return JsonResponse({'status': False, 'code': 'timeout', 'message': 'API request timed out'})
    except requests.exceptions.ConnectionError:
        print("we are in 6")

        return JsonResponse({'status': False, 'code': 'connection_error', 'message': 'API connection error'})


def verify(request):
    authority = request.GET.get('Authority')
    data = request.session.get('data')
    print("data in 11 is:", data)
    amount = data.get('Amount')
    print("amount is:", amount)
    data.update({"Authority": authority})
    data = json.dumps(data)
    print("data in 12 is:", data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            print("we are in verify view with status 100.")

            invoice = InvoiceModel(user=request.user, payment_status=True, amount=amount, refid=response['RefID'])
            invoice.save()

            empty_cart_url = 'http://127.0.0.1:8000/cart/empty'
            response = requests.delete(empty_cart_url)    # test this.

            return JsonResponse({'status': True, 'RefID': response['RefID']})
        else:
            return JsonResponse({'status': False, 'code': str(response['Status'])})
    return HttpResponse(response.content, status=response.status_code)


class PaymentView(APIView):
    def get(self, request):

        print("PaymentView/def get: we have arrived")
        url = request.GET.get('response')
        print("the url which we passed to get is:", url)
        if url:
            encoded_url = urllib.parse.quote(url, safe=':/')
            print(encoded_url)
            return redirect(encoded_url)
        else:
            pass
        # url = "https://sandbox.zarinpal.com/pg/StartPay/000000000000000000000000000001412253"
        # return redirect(url)
        status = request.query_params.get('Status')
        print("here the status is:", status)
        authority = request.query_params.get('Authority')
        print("we are at 9")

        if status == '100':
            print("we are at 10")
            # Payment was successful
            # ... your code ...
            return Response({'message': 'Payment successful'})
        else:
            # Payment was not successful
            # ... your code ...
            return Response({'message': 'Payment failed'})  # when we first reach PaymentView endpoint, the code
                                                            # goes through get method and returns this message

    def post(self, request):
        # Handle POST requests to /pay/pai/
        phone_number = request.data.get('phone_number')
        email = request.data.get('email')
        description = request.data.get('description')
        if not description:
            description = "something"

        amount = request.session.get('Amount')
        if not amount:
            amount = request.session.get('final_price')
        print("final price is:", amount)
        data = {
            "Phone_number": phone_number,
            "Email": email,
            "Description": description,
            'Amount': amount,
        }

        request.session['data'] = data
        request.session.modified = True

        response = send_request(request)

        print("response is:", response)
        if response.status_code == 200:
            print("we are in Payment def post. status is 200 ")
            middle_pay_url = reverse('middle') + '?response={}'.format(response.content.decode())
            print('middle pay url is:', middle_pay_url)
            return redirect(middle_pay_url)
            # response_data = json.loads(response.content)
            # if response_data.get('status'):
            #     print("we are in Payment def post. status is: ", response_data.get('status'))
            #     payment_url = response_data.get('url')
            #     print("payment_url", payment_url)
            #     return redirect(payment_url)
            # else:
            #     print("we are at 7")
            #     error_code = response_data.get('code')
            #     print(error_code)
            #     return Response({'message': 'Payment failed'})

        else:
            error_message = "API request failed with status code: {}".format(response.status_code)
            print(error_message)
            return Response({'error': error_message})


class MiddlePayView(APIView):
    def get(self, request):
        print("we are in MiddlePayView now!")
        response = request.GET.get('response')
        print("here response is:", response)

        response_data = json.loads(response)
        if response_data.get('status'):
            print("we are in MiddlePayView def get. status is: ", response_data.get('status'))
            payment_url = response_data.get('url')
            print("payment_url", payment_url)
            # return redirect(payment_url)
            payment_view_url = reverse('paying') + '?response=' + quote(payment_url)
            print('middle pay url is:', payment_view_url)
            return redirect(payment_view_url)
            # return HttpResponseRedirect(payment_url)
        else:
            print("we are at 7")
            error_code = response_data.get('code')
            print(error_code)
            return Response({'message': 'Payment failed'})


# def payment_view(request):
#     response = send_request(request)
#     if response.status_code == 200:
#         response_data = json.loads(response.content)
#         if response_data.get('status'):
#             payment_url = response_data.get('url')
#             return redirect(payment_url)
#         else:
#             error_code = response_data.get('code')
#     else:
#         error_message = "API request failed with status code: {}".format(response.status_code)
class DiscountCodeApplyView(APIView):
    def post(self, request):
        discount_code = request.data.get('discount_code')

        try:
            discount = DiscountCodeModel.objects.get(discount_code=discount_code, avalable=True)
            final_price = request.session.get('final_price')
            amount = str(final_price * (100 - discount.percentage))
            request.session['Amount'] = amount
            request.session.modified = True

            serializer = DiscountCodeSerializer(discount)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except DiscountCodeModel.DoesNotExist:
            return Response({'error': ' Invalid code'}, status=status.HTTP_400_BAD_REQUEST)


