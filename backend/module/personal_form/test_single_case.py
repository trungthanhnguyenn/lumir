#!/usr/bin/env python3
"""
Simple test script for a single case
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bulk_api_test import BulkAPITester

def test_single_case():
    """Test a single case"""
    
    # Test case
    test_case = {
        "name": "Test Case - Huỳnh Đăng Nghĩa",
        "payload": {
            "full_name": "Huỳnh Đăng Nghĩa",
            "date_of_birth": "27/10/2002",
            "current_date": "07/08/2025"
        }
    }
    
    # Create tester and run test
    tester = BulkAPITester()
    result = tester.test_single_payload(test_case["payload"], test_case["name"])
    
    return result

if __name__ == "__main__":
    test_single_case()
