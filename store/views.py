from django.shortcuts import render
import requests
import base64
from datetime import datetime
from django.http import JsonResponse
from requests.auth import HTTPBasicAuth
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def index(request):
    return render(request, 'store/index.html')

def about(request):
    return render(request, 'store/about.html')

def cart(request):
    return render(request, 'store/cart.html')

def cassetteplayers(request):
    return render(request, 'store/cassetteplayers.html')

def contact(request):
    return render(request, 'store/contact.html')

def faq(request):
    return render(request, 'store/faq.html')

def login(request):
    return render(request, 'store/login.html')

def policy(request):
    return render(request, 'store/policy.html')
# M-Pesa credentials
consumer_key = 'YOUR_CONSUMER_KEY'
consumer_secret = 'YOUR_CONSUMER_SECRET'
business_short_code = '174379'  # Lipa Na M-Pesa Short Code
lipa_na_mpesa_online_passkey = 'YOUR_PASSKEY'

# Generate access token
def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    json_response = response.json()
    return json_response['access_token']

# Create the password
def generate_password():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_encode = business_short_code + lipa_na_mpesa_online_passkey + timestamp
    return base64.b64encode(data_to_encode.encode()).decode('utf-8')

@csrf_exempt
def mpesa_checkout(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone')
        amount = request.POST.get('amount')
        
        access_token = get_access_token()
        headers = {"Authorization": "Bearer %s" % access_token}
        
        payload = {
            "BusinessShortCode": business_short_code,
            "Password": generate_password(),
            "Timestamp": datetime.now().strftime('%Y%m%d%H%M%S'),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": business_short_code,
            "PhoneNumber": phone_number,
            "CallBackURL": "https://example.com/callback",  # Replace with your callback
            "AccountReference": "Vinyl Purchase",
            "TransactionDesc": "Payment for Vinyl"
        }
        
        response = requests.post("https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest", json=payload, headers=headers)
        return JsonResponse(response.json())

