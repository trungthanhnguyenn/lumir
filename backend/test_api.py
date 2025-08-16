#!/usr/bin/env python3
"""
Quick test script for the numerology API
"""

import requests
import json

def test_api():
    """Test the numerology API endpoint"""
    
    # API endpoint
    url = "http://localhost:8000/api/v1/numerology/calculate"
    
    # Test payload
    payload = {
        "full_name": "Nguyễn Văn A",
        "date_of_birth": "15/06/1995",
        "current_date": "20/12/2024"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("🧪 Testing Numerology API...")
        print(f"URL: {url}")
        print(f"Payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")
        print("-" * 50)
        
        # Make request
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API Response:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
            # Check response structure
            if result.get("success") and "data" in result:
                print("\n✅ Response structure is correct!")
                if "pwi_indices" in result["data"]:
                    print("✅ PWI indices found!")
                    indices = result["data"]["pwi_indices"]
                    print(f"✅ Found {len(indices)} numerology indices")
                else:
                    print("❌ PWI indices missing")
            else:
                print("❌ Response structure incorrect")
        else:
            print(f"❌ API Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the API server is running on port 8000")
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: Request took too long")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    test_api()
