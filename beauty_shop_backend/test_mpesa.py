"""
Test script to verify M-Pesa STK Push integration
Run this to debug M-Pesa issues
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add app to path
sys.path.insert(0, os.path.dirname(__file__))

from app.utils.mpesa import initiate_stk_push, get_access_token

def test_credentials():
    """Test if credentials are loaded correctly"""
    print("=" * 60)
    print("1. TESTING ENVIRONMENT VARIABLES")
    print("=" * 60)
    
    credentials = {
        "MPESA_CONSUMER_KEY": os.getenv("MPESA_CONSUMER_KEY"),
        "MPESA_CONSUMER_SECRET": os.getenv("MPESA_CONSUMER_SECRET"),
        "MPESA_SHORTCODE": os.getenv("MPESA_SHORTCODE"),
        "MPESA_PASSKEY": os.getenv("MPESA_PASSKEY"),
        "MPESA_CALLBACK_URL": os.getenv("MPESA_CALLBACK_URL")
    }
    
    all_set = True
    for key, value in credentials.items():
        if value:
            # Mask sensitive values
            if key in ["MPESA_CONSUMER_SECRET", "MPESA_PASSKEY"]:
                display_value = value[:10] + "..." if len(value) > 10 else "***"
            else:
                display_value = value
            print(f"✓ {key}: {display_value}")
        else:
            print(f"✗ {key}: NOT SET")
            all_set = False
    
    print()
    return all_set

def test_access_token():
    """Test if we can get access token from Safaricom"""
    print("=" * 60)
    print("2. TESTING ACCESS TOKEN")
    print("=" * 60)
    
    access_token, error = get_access_token()
    
    if error:
        print(f"✗ FAILED: {error.get('errorMessage')}")
        print(f"  Error Code: {error.get('errorCode')}")
        return False
    else:
        print(f"✓ SUCCESS: Got access token")
        print(f"  Token (first 20 chars): {access_token[:20]}...")
        print()
        return True

def test_stk_push():
    """Test STK Push with a sample phone number"""
    print("=" * 60)
    print("3. TESTING STK PUSH")
    print("=" * 60)
    
    # Use test phone number for sandbox
    test_phone = "254708374149"  # Safaricom test number
    test_amount = 1
    test_invoice = "TEST-" + str(int(os.urandom(4).hex(), 16))[:8]
    
    print(f"Phone: {test_phone}")
    print(f"Amount: KES {test_amount}")
    print(f"Invoice: {test_invoice}")
    print()
    
    result = initiate_stk_push(
        phone=test_phone,
        amount=test_amount,
        invoice_no=test_invoice
    )
    
    print("Response:")
    print("-" * 60)
    
    # Check if successful
    if result.get("ResponseCode") == "0":
        print("✓ SUCCESS: STK Push initiated")
        print(f"  Checkout Request ID: {result.get('CheckoutRequestID')}")
        print(f"  Merchant Request ID: {result.get('MerchantRequestID')}")
        print(f"  Response Description: {result.get('ResponseDescription')}")
        return True
    elif result.get("errorCode"):
        print(f"✗ FAILED: {result.get('errorMessage')}")
        print(f"  Error Code: {result.get('errorCode')}")
        return False
    else:
        print("✗ FAILED: Unexpected response")
        import json
        print(json.dumps(result, indent=2))
        return False

def main():
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "M-PESA STK PUSH TEST" + " " * 23 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    # Step 1: Check credentials
    if not test_credentials():
        print("\n⚠ WARNING: Some credentials are missing!")
        print("Please check your .env file in beauty_shop_backend/")
        return
    
    # Step 2: Test access token
    if not test_access_token():
        print("\n⚠ Cannot proceed without access token")
        return
    
    # Step 3: Test STK push
    test_stk_push()
    
    print()
    print("=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
    print()

if __name__ == "__main__":
    main()
