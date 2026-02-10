import requests
import base64
from datetime import datetime
import os

class MpesaDaraja:
    def __init__(self):
        self.consumer_key = os.getenv('MPESA_CONSUMER_KEY')
        self.consumer_secret = os.getenv('MPESA_CONSUMER_SECRET')
        self.shortcode = os.getenv('MPESA_SHORTCODE')
        self.passkey = os.getenv('MPESA_PASSKEY')
        self.callback_url = os.getenv('MPESA_CALLBACK_URL', 'https://yourdomain.com/api/mpesa/callback')
        
        # Sandbox URLs (change to production when ready)
        self.auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
        self.stk_push_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    
    def get_access_token(self):
        """Get OAuth access token from Daraja API"""
        try:
            auth_string = f"{self.consumer_key}:{self.consumer_secret}"
            encoded = base64.b64encode(auth_string.encode()).decode()
            
            headers = {
                'Authorization': f'Basic {encoded}'
            }
            
            response = requests.get(self.auth_url, headers=headers)
            response.raise_for_status()
            
            return response.json()['access_token']
        except Exception as e:
            print(f"Error getting access token: {e}")
            return None
    
    def initiate_stk_push(self, phone_number, amount, account_reference, transaction_desc):
        """
        Initiate STK Push to customer's phone
        
        Args:
            phone_number: Format 254712345678
            amount: Amount to charge
            account_reference: Order ID or reference
            transaction_desc: Description of transaction
        """
        access_token = self.get_access_token()
        if not access_token:
            return {'success': False, 'message': 'Failed to get access token'}
        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password_string = f"{self.shortcode}{self.passkey}{timestamp}"
        password = base64.b64encode(password_string.encode()).decode()
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": self.callback_url,
            "AccountReference": account_reference,
            "TransactionDesc": transaction_desc
        }
        
        try:
            response = requests.post(self.stk_push_url, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('ResponseCode') == '0':
                return {
                    'success': True,
                    'message': 'STK Push sent successfully',
                    'checkout_request_id': result.get('CheckoutRequestID'),
                    'merchant_request_id': result.get('MerchantRequestID')
                }
            else:
                return {
                    'success': False,
                    'message': result.get('ResponseDescription', 'STK Push failed')
                }
        except Exception as e:
            print(f"Error initiating STK Push: {e}")
            return {
                'success': False,
                'message': str(e)
            }

# Usage example
def send_mpesa_prompt(phone, amount, order_id):
    """
    Send real M-Pesa prompt to customer's phone
    
    Args:
        phone: Customer phone number (254712345678)
        amount: Amount to charge
        order_id: Order reference
    
    Returns:
        dict: Response with success status and details
    """
    mpesa = MpesaDaraja()
    result = mpesa.initiate_stk_push(
        phone_number=phone,
        amount=amount,
        account_reference=order_id,
        transaction_desc=f"Payment for order {order_id}"
    )
    return result
