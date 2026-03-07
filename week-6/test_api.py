#!/usr/bin/env python3
"""
Test script to demonstrate correct API usage for creating notes
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:5000"

def test_create_note():
    """Test creating a note with correct format"""

    # First, register a user
    register_data = {
        "username": "testuser",
        "password": "Testpass1"
    }

    print("1. Registering user...")
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            print("   ✅ User registered successfully")
        elif response.status_code == 409:
            print("   ℹ️  User already exists")
        else:
            print(f"   ❌ Registration failed: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
        return

    # Login to get token
    print("\n2. Logging in...")
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=register_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            token = response.json().get('access_token')
            print("   ✅ Login successful, got token")
        else:
            print(f"   ❌ Login failed: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
        return

    # Test correct note creation
    print("\n3. Creating note with CORRECT format...")
    headers = {"Authorization": f"Bearer {token}"}
    correct_note = {
        "title": "My Test Note",
        "content": "This is the content of my test note."
    }

    try:
        response = requests.post(f"{BASE_URL}/notes", json=correct_note, headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            print("   ✅ Note created successfully!")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ❌ Note creation failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Connection error: {e}")

    # Test incorrect note creation (using 'subject' instead of 'title')
    print("\n4. Testing INCORRECT format (using 'subject' instead of 'title')...")
    incorrect_note = {
        "subject": "My Test Note",  # Wrong field name!
        "content": "This should fail because 'subject' is not a valid field."
    }

    try:
        response = requests.post(f"{BASE_URL}/notes", json=incorrect_note, headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        if "subject" in response.text.lower():
            print("   ❌ This shows the error you're seeing!")
    except Exception as e:
        print(f"   ❌ Connection error: {e}")

if __name__ == "__main__":
    print("🔍 Testing User Notes API")
    print("=" * 50)
    test_create_note()