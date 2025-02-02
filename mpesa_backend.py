from flask import Flask, request, jsonify
import requests
from requests.auth import HTTPBasicAuth
import base64
from datetime import datetime

app = Flask(__name__)

# M-Pesa credentials (for sandbox testing)
consumer_key = 'YOUR_CONSUMER_KEY'
consumer_secret = 'YOUR_CONSUMER_SECRET'
business_short_code = '174379'  # Test PayBill or Lipa Na M-Pesa
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

# M-Pesa Payment Request
@app.route('/mpesa_checkout', methods=['POST'])
def mpesa_checkout():
    phone_number = request.json['phone']
    amount = request.json['amount']
    
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
        "CallBackURL": "https://example.com/callback",  # Your callback URL
        "AccountReference": "Vinyl Purchase",
        "TransactionDesc": "Payment for Vinyl"
    }
    
    response = requests.post("https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest", json=payload, headers=headers)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
