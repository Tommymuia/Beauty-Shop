import requests
import base64
from datetime import datetime
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Get logger for this module
logger = logging.getLogger(__name__)

# Safaricom Sandbox Credentials from environment
CONSUMER_KEY = os.getenv("MPESA_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("MPESA_CONSUMER_SECRET")
BUSINESS_SHORTCODE = os.getenv("MPESA_SHORTCODE")
PASSKEY = os.getenv("MPESA_PASSKEY")
CALLBACK_URL = os.getenv("MPESA_CALLBACK_URL")

def get_access_token():
    """
    Get M-Pesa access token for API authentication.
    
    Returns:
        tuple: (access_token, error_dict) - One will be None if there's an error
    """
    # Validate credentials
    if not all([CONSUMER_KEY, CONSUMER_SECRET]):
        error = {
            "errorCode": "500",
            "errorMessage": "M-Pesa credentials not configured. Check MPESA_CONSUMER_KEY and MPESA_CONSUMER_SECRET in .env"
        }
        logger.error(error["errorMessage"])
        return None, error
    
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
    try:
        response = requests.get(url, auth=(CONSUMER_KEY, CONSUMER_SECRET), timeout=10)
        response.raise_for_status()
        
        access_token = response.json().get("access_token")
        if not access_token:
            error = {"errorCode": "500", "errorMessage": "No access token in M-Pesa response"}
            logger.error(error["errorMessage"])
            return None, error
            
        logger.info("Successfully obtained M-Pesa access token")
        return access_token, None
        
    except requests.exceptions.Timeout:
        error = {"errorCode": "504", "errorMessage": "M-Pesa authentication request timed out"}
        logger.error(error["errorMessage"])
        return None, error
    except requests.exceptions.ConnectionError as e:
        error = {"errorCode": "500", "errorMessage": f"Cannot connect to M-Pesa service: {str(e)}"}
        logger.error(error["errorMessage"])
        return None, error
    except requests.exceptions.HTTPError as e:
        error = {"errorCode": "500", "errorMessage": f"M-Pesa authentication failed: {str(e)}"}
        logger.error(error["errorMessage"])
        return None, error
    except Exception as e:
        error = {"errorCode": "500", "errorMessage": f"Unexpected error getting M-Pesa token: {str(e)}"}
        logger.error(error["errorMessage"])
        return None, error

def initiate_stk_push(phone: str, amount: int, invoice_no: str):
    """
    Initiate M-Pesa STK Push to customer's phone.
    
    Args:
        phone: Customer phone number (07... or 254...)
        amount: Amount to charge
        invoice_no: Invoice/order reference number
        
    Returns:
        dict: Response from M-Pesa API
    """
    # Validate required configuration
    if not all([BUSINESS_SHORTCODE, PASSKEY, CALLBACK_URL]):
        missing = []
        if not BUSINESS_SHORTCODE: missing.append("MPESA_SHORTCODE")
        if not PASSKEY: missing.append("MPESA_PASSKEY")
        if not CALLBACK_URL: missing.append("MPESA_CALLBACK_URL")
        error_msg = f"M-Pesa configuration incomplete. Missing: {', '.join(missing)}"
        logger.error(error_msg)
        return {
            "errorCode": "500",
            "errorMessage": error_msg
        }
    
    # 1. Get Access Token
    access_token, token_error = get_access_token()
    if token_error:
        return token_error
    
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    
    # 2. Format Phone Number (Handle None, 07..., +254...)
    if not phone:
        logger.error("Phone number is None or empty")
        return {"errorCode": "400", "errorMessage": "PhoneNumber is None"}
        
    clean_phone = str(phone).strip().replace("+", "")
    if clean_phone.startswith("0"):
        clean_phone = "254" + clean_phone[1:]
    
    # Validate phone number format
    if not clean_phone.startswith("254") or len(clean_phone) != 12:
        logger.error(f"Invalid phone number format: {phone}")
        return {
            "errorCode": "400",
            "errorMessage": "Invalid phone number format. Expected format: 254712345678"
        }
    
    logger.info(f"Initiating STK push for phone: {clean_phone}, amount: {amount}, invoice: {invoice_no}")
    
    # 3. Security Credentials
    password_str = BUSINESS_SHORTCODE + PASSKEY + timestamp
    password = base64.b64encode(password_str.encode()).decode('utf-8')
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    payload = {
        "BusinessShortCode": BUSINESS_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": clean_phone, 
        "PartyB": BUSINESS_SHORTCODE,
        "PhoneNumber": clean_phone,
        "CallBackURL": CALLBACK_URL, 
        "AccountReference": invoice_no,
        "TransactionDesc": "Beauty Shop Purchase"
    }

    try:
        response = requests.post(
            "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
            json=payload,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        logger.info(f"STK Push response: {result}")
        return result
        
    except requests.exceptions.Timeout:
        logger.error("M-Pesa API request timed out")
        return {
            "errorCode": "504",
            "errorMessage": "Request timed out. Please try again."
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error during STK push: {e}")
        return {
            "errorCode": "500",
            "errorMessage": f"Network error: {str(e)}"
        }
    except Exception as e:
        logger.error(f"Unexpected error during STK push: {e}")
        return {
            "errorCode": "500",
            "errorMessage": f"Unexpected error: {str(e)}"
        }