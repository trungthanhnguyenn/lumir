#!/bin/bash

# Lumir AI Numerology API Test Script
# Test the API endpoints using curl

BASE_URL="http://localhost:8686"

echo "🔮 Lumir AI Numerology API - Curl Tests"
echo "========================================"
echo "Base URL: $BASE_URL"
echo ""

# Test 1: Health Check
echo "🏥 Test 1: Health Check"
echo "-----------------------"
curl -s -X GET "$BASE_URL/health" | jq .
echo ""

# Test 2: Numerology Health Check
echo "🔮 Test 2: Numerology Health Check"
echo "----------------------------------"
curl -s -X GET "$BASE_URL/api/v1/numerology/health" | jq .
echo ""

# Test 3: Basic Numerology Calculation
echo "🧮 Test 3: Basic Numerology Calculation"
echo "--------------------------------------"
curl -s -X POST "$BASE_URL/api/v1/numerology/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Nguyễn Văn A",
    "date_of_birth": "15/06/1995",
    "current_date": "20/12/2024"
  }' | jq .
echo ""

# Test 4: Complex Vietnamese Name
echo "🧮 Test 4: Complex Vietnamese Name"
echo "----------------------------------"
curl -s -X POST "$BASE_URL/api/v1/numerology/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Huỳnh Đăng Nghĩa",
    "date_of_birth": "27/10/2002",
    "current_date": "07/08/2025"
  }' | jq .
echo ""

# Test 5: Without Current Date
echo "🧮 Test 5: Without Current Date"
echo "-------------------------------"
curl -s -X POST "$BASE_URL/api/v1/numerology/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Trần Thị B",
    "date_of_birth": "03/01/2003"
  }' | jq .
echo ""

# Test 6: Validation Error - Empty Name
echo "⚠️ Test 6: Validation Error - Empty Name"
echo "----------------------------------------"
curl -s -X POST "$BASE_URL/api/v1/numerology/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "",
    "date_of_birth": "15/06/1995"
  }' | jq .
echo ""

# Test 7: Validation Error - Invalid Date Format
echo "⚠️ Test 7: Validation Error - Invalid Date Format"
echo "------------------------------------------------"
curl -s -X POST "$BASE_URL/api/v1/numerology/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Nguyễn Văn A",
    "date_of_birth": "15-06-1995"
  }' | jq .
echo ""

echo "✅ All tests completed!"
echo ""
echo "💡 To run individual tests, copy the curl commands above."
echo "💡 Make sure jq is installed for pretty JSON output: sudo apt install jq"
