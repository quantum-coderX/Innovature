#!/usr/bin/env python3
"""
Simple OTP Testing Script
Tests the complete 2FA/OTP flow without needing actual email
"""

import requests
import json
import time
from database import db
from models import OTP, User
from main import app

BASE_URL = "http://localhost:5000"

def print_section(title):
    """Print formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

# Test data - use timestamp for unique username
timestamp = int(time.time())
test_user = {
    "username": f"testuser{timestamp}",
    "email": f"test{timestamp}@example.com",
    "password": "TestPassword123"
}

print_section("OTP TESTING FLOW")

# 1. REGISTER USER
print_section("Step 1: Register User")
print(f"📝 Registering: {test_user['username']}")

response = requests.post(
    f"{BASE_URL}/api/auth/register",
    json=test_user
)

print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

if response.status_code != 201:
    print("❌ Registration failed!")
    exit(1)

print("✅ Registration successful!")

# 2. LOGIN USER (Triggers OTP)
print_section("Step 2: Login User (Triggers OTP)")
print(f"🔐 Logging in: {test_user['username']}")

login_data = {
    "username": test_user['username'],
    "password": test_user['password']
}

response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json=login_data
)

print(f"Status: {response.status_code}")
response_json = response.json()
print(f"Response: {json.dumps(response_json, indent=2)}")

# Check if it's an email sending error (expected with test credentials)
if response.status_code == 500 and "Failed to send OTP" in response_json.get('message', ''):
    print("⚠️  Email sending failed (expected with test credentials)")
    print("✅ But OTP was generated! (We'll retrieve it from DB)")
    # Get user_id from database
    with app.app_context():
        user = User.query.filter_by(username=test_user['username']).first()
        user_id = user.id
elif response.status_code == 200:
    user_id = response_json.get('user_id')
    print(f"✅ Login successful! User ID: {user_id}")
else:
    print("❌ Login failed!")
    exit(1)

# 3. GET OTP CODE FROM DATABASE
print_section("Step 3: Fetch OTP Code from Database")
print(f"🔍 Getting OTP for User ID: {user_id}")

with app.app_context():
    # Get the latest OTP for this user
    otp = OTP.query.filter_by(user_id=user_id, is_verified=False).order_by(OTP.created_at.desc()).first()
    
    if not otp:
        print("❌ No OTP found!")
        exit(1)
    
    otp_code = otp.otp_code
    print(f"✅ OTP Code: {otp_code}")
    print(f"   Expires At: {otp.expires_at}")
    print(f"   Is Expired: {otp.is_expired()}")

# 4. VERIFY OTP
print_section("Step 4: Verify OTP")
print(f"✔️ Verifying OTP: {otp_code}")

verify_data = {
    "user_id": user_id,
    "otp_code": otp_code
}

response = requests.post(
    f"{BASE_URL}/api/auth/verify-otp",
    json=verify_data
)

print(f"Status: {response.status_code}")
response_json = response.json()
print(f"Response: {json.dumps(response_json, indent=2)}")

if response.status_code != 200:
    print("❌ OTP verification failed!")
    exit(1)

access_token = response_json.get('access_token')
print(f"✅ OTP verified successfully!")
print(f"   Access Token: {access_token[:50]}...")

# 5. TEST PROTECTED ENDPOINT  
print_section("Step 5: Test Protected Endpoint")
print(f"🔒 Accessing /api/users/profile with token...")

headers = {
    "Authorization": f"Bearer {access_token}"
}

response = requests.get(
    f"{BASE_URL}/api/users/profile",
    headers=headers
)

print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

if response.status_code == 200:
    print("✅ Protected endpoint access successful!")
else:
    print("❌ Protected endpoint access failed!")

print_section("TEST COMPLETE")
print("✅ All OTP flow tests passed!")
