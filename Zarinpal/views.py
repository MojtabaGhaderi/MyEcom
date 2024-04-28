from django.conf import settings
import requests
import json

from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse

# ? sandbox merchant
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

amount = 1000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
phone = 'YOUR_PHONE_NUMBER'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/pay/verify/'





def send_request(request):
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": amount,
        "Description": description,
        "Phone": phone,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response_data = response.json()
            if response_data['Status'] == 100:
                return JsonResponse({'status': True, 'url': ZP_API_STARTPAY + str(response_data['Authority']),
                                     'authority': response_data['Authority']})
            else:
                return JsonResponse({'status': False, 'code': str(response_data['Status'])})
        return HttpResponse(response.content, status=response.status_code)

    except requests.exceptions.Timeout:
        return JsonResponse({'status': False, 'code': 'timeout'})
    except requests.exceptions.ConnectionError:
        return JsonResponse({'status': False, 'code': 'connection error'})


def verify(request):
    authority = request.GET.get('Authority')
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": amount,
        "Authority": authority,
    }
    print("authourity:", authority)
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            return JsonResponse({'status': True, 'RefID': response['RefID']})
        else:
            return JsonResponse({'status': False, 'code': str(response['Status'])})
    return HttpResponse(response.content, status=response.status_code)


def payment_view(request):
    response = send_request(request)
    if response.status_code == 200:
        response_data = json.loads(response.content)
        if response_data.get('status'):
            payment_url = response_data.get('url')
            return redirect(payment_url)
        else:
            # Handle the case when payment request fails
            error_code = response_data.get('code')
            # Render an error page or perform any necessary actions
    else:
        # Handle the case when the API request fails
        error_message = "API request failed with status code: {}".format(response.status_code)
        # Render an error page or perform any necessary actions