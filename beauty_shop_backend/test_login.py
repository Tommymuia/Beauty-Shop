"""
Quick script to test login and create a test user if needed
"""
import requests

BASE_URL = "http://localhost:8000/api"

# Test credentials
test_email = "test@example.com"
test_password = "password123"

print("=" * 50)
print("LOGIN DIAGNOSTIC TOOL")
print("=" * 50)

# 1. Check if backend is running
print("\n1. Checking if backend is running...")
try:
    response = requests.get("http://localhost:8000/")
    print(f"✓ Backend is running: {response.json()}")
except Exception as e:
    print(f"✗ Backend is NOT running: {e}")
    print("  → Start your backend server first!")
    exit(1)

# 2. Try to register a test user
print(f"\n2. Attempting to register test user: {test_email}")
try:
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={"email": test_email, "password": test_password}
    )
    if response.status_code == 200:
        print(f"✓ Test user registered successfully")
        print(f"  Token: {response.json().get('access_token')[:20]}...")
    elif response.status_code == 400:
        print(f"⚠ User already exists (this is OK)")
    else:
        print(f"✗ Registration failed: {response.status_code}")
        print(f"  Response: {response.text}")
except Exception as e:
    print(f"✗ Registration error: {e}")

# 3. Try to login
print(f"\n3. Attempting login with: {test_email}")
try:
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": test_email, "password": test_password}
    )
    if response.status_code == 200:
        print(f"✓ Login successful!")
        token = response.json().get('access_token')
        print(f"  Token: {token[:20]}...")
        
        # 4. Try to access protected route
        print(f"\n4. Testing protected route (/auth/me)")
        me_response = requests.get(
            f"{BASE_URL}/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        if me_response.status_code == 200:
            print(f"✓ Protected route works!")
            print(f"  User: {me_response.json()}")
        else:
            print(f"✗ Protected route failed: {me_response.status_code}")
            print(f"  Response: {me_response.text}")
    else:
        print(f"✗ Login failed: {response.status_code}")
        print(f"  Response: {response.text}")
except Exception as e:
    print(f"✗ Login error: {e}")

# 5. Test with wrong password
print(f"\n5. Testing with wrong password (should fail)")
try:
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": test_email, "password": "wrongpassword"}
    )
    if response.status_code == 401:
        print(f"✓ Correctly rejected wrong password")
    else:
        print(f"⚠ Unexpected response: {response.status_code}")
        print(f"  Response: {response.text}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "=" * 50)
print("DIAGNOSIS COMPLETE")
print("=" * 50)
print("\nIf all tests passed, your auth system is working correctly.")
print("If tests failed, check the error messages above.")
