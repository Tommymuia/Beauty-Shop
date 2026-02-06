import requests
import base64
from datetime import datetime
from fastapi import HTTPException

# Safaricom Sandbox Credentials
CONSUMER_KEY = "DOnqU2TATzAnyOaAFfL9ZANLdYTUQr1FziEa8KckWDvMn7es" 
CONSUMER_SECRET = "hu7Jrl1qvuhip30ygRumkqVzdgsoMAeBtjRaFllXwWxa50ttOGw1R8tuoXyEqHv8" 
BUSINESS_SHORTCODE = "174379"
PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"

def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=(CONSUMER_KEY, CONSUMER_SECRET))
    if response.status_code == 200:
        return response.json().get("access_token")
    raise HTTPException(status_code=500, detail="Failed to fetch M-Pesa token")

def initiate_stk_push(phone: str, amount: int, invoice_no: str):
    access_token = get_access_token()
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    
    # Password must be Base64(ShortCode + Passkey + Timestamp)
    password_str = BUSINESS_SHORTCODE + PASSKEY + timestamp
    password = base64.b64encode(password_str.encode()).decode('utf-8')
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    payload = {
        "BusinessShortCode": BUSINESS_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone, # Phone number must be 2547XXXXXXXX
        "PartyB": BUSINESS_SHORTCODE,
        "PhoneNumber": phone,
        "CallBackURL": "https://mydomain.com/api/orders/callback", 
        "AccountReference": invoice_no,
        "TransactionDesc": "Beauty Shop Purchase"
    }

    response = requests.post(
        "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
        json=payload,
        headers=headers
    )
    return response.json()