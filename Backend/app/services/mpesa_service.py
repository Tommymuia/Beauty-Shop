import requests
import base64
from datetime import datetime
from typing import Optional
import os

class MpesaService:
    def __init__(self):  # FIXED
        self.consumer_key = os.getenv("MPESA_CONSUMER_KEY", "")  # FIXED
        self.consumer_secret = os.getenv("MPESA_CONSUMER_SECRET", "")
        self.business_short_code = os.getenv("MPESA_BUSINESS_SHORT_CODE", "174379")
        self.passkey = os.getenv("MPESA_PASSKEY", "")
        self.callback_url = os.getenv("MPESA_CALLBACK_URL", "https://yourdomain.com/api/v1/mpesa/callback")
        self.auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        self.stk_push_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    
    def get_access_token(self) -> Optional[str]:
        """Get access token from Safaricom API"""
        try:
            credentials = base64.b64encode(f"{self.consumer_key}:{self.consumer_secret}".encode()).decode()  # FIXED
            headers = {
                "Authorization": f"Basic {credentials}",  # FIXED
                "Content-Type": "application/json"
            }
            
            response = requests.get(self.auth_url, headers=headers)
            if response.status_code == 200:
                return response.json().get("access_token")  # FIXED
            return None
        except Exception as e:
            print(f"Error getting access token: {e}")
            return None
    
    def generate_password(self) -> tuple:
        """Generate password and timestamp for STK push"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password_string = f"{self.business_short_code}{self.passkey}{timestamp}"
        password = base64.b64encode(password_string.encode()).decode()
        return password, timestamp
    
    def initiate_stk_push(self, phone_number: str, amount: float, order_id: str) -> dict:
        """Initiate STK push payment"""
        access_token = self.get_access_token()
        if not access_token:
            return {"success": False, "message": "Failed to get access token"}  # FIXED
        
        password, timestamp = self.generate_password()
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "BusinessShortCode": self.business_short_code,  # FIXED
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": phone_number,
            "PartyB": self.business_short_code,
            "PhoneNumber": phone_number,
            "CallBackURL": self.callback_url,
            "AccountReference": f"ORDER-{order_id}",
            "TransactionDesc": f"Payment for order {order_id}"
        }
        
        try:
            response = requests.post(self.stk_push_url, json=payload, headers=headers)
            return response.json()
        except Exception as e:
            return {"success": False, "message": f"STK push failed: {e}"}
    
    def query_transaction_status(self, checkout_request_id: str) -> dict:
        """Query the status of a transaction"""
        return {"success": True, "status": "pending"}

mpesa_service = MpesaService()