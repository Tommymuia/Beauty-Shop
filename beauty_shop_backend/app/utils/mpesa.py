import requests
import base64
from datetime import datetime
from fastapi import HTTPException
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

def get_access_token():
    """
    Get M-Pesa access token for API authentication.
    
    Returns:
        str: Access token
        
    Raises:
        HTTPException: If token fetch fails
    """
    # Validate credentials
    if not all([CONSUMER_KEY, CONSUMER_SECRET]):
        logger.error("M-Pesa credentials are missing. Please check MPESA_CONSUMER_KEY and MPESA_CONSUMER_SECRET in .env file")
        raise HTTPException(status_code=500, detail="M-Pesa credentials not configured")
    
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
    try:
        response = requests.get(url, auth=(CONSUMER_KEY, CONSUMER_SECRET), timeout=10)
        response.raise_for_status()
        
        access_token = response.json().get("access_token")
        if not access_token:
            logger.error("Access token not found in M-Pesa response")
            raise HTTPException(status_code=500, detail="Failed to fetch M-Pesa token")
            
        logger.info("Successfully obtained M-Pesa access token")
        return access_token
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error while fetching M-Pesa token: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch M-Pesa token: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error while fetching M-Pesa token: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch M-Pesa token")

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
    if not all([BUSINESS_SHORTCODE, PASSKEY]):
        logger.error("M-Pesa configuration is incomplete. Please check MPESA_SHORTCODE and MPESA_PASSKEY in .env file")
        return {
            "errorCode": "500",
            "errorMessage": "M-Pesa configuration incomplete"
        }
    
    # 1. Access Token
    try:
        access_token = get_access_token()
    except HTTPException as e:
        logger.error(f"Failed to get access token: {e.detail}")
        return {
            "errorCode": "500",
            "errorMessage": f"Authentication failed: {e.detail}"
        }
    
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
    
    # Get callback URL from environment, fallback to a default
    callback_url = os.getenv("MPESA_CALLBACK_URL", "https://REPLACE_WITH_YOUR_DOMAIN.com/api/orders/mpesa/callback")
    
    payload = {
        "BusinessShortCode": BUSINESS_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": clean_phone, 
        "PartyB": BUSINESS_SHORTCODE,
        "PhoneNumber": clean_phone,
        "CallBackURL": callback_url, 
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