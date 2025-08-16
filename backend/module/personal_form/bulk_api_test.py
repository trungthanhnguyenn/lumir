#!/usr/bin/env python3
"""
Bulk API Testing Script

This script tests multiple payloads against the API and compares results
with local cal_num calculations to ensure formula accuracy.
"""

import sys
import os
import requests
import json
import time
from typing import Dict, List, Any
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cal_num import CalNum

class BulkAPITester:
    """Bulk API testing and comparison class"""
    
    def __init__(self, api_url: str = "https://ftmo-api-dev.buso.asia/api/v1/pwi/calculate"):
        self.api_url = api_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'BulkAPITester/1.0'
        })
    
    def call_api(self, payload: Dict[str, str]) -> Dict[str, Any]:
        """
        Call the API with given payload
        
        Args:
            payload: Dictionary containing full_name, date_of_birth, current_date
            
        Returns:
            API response as dictionary
        """
        try:
            response = self.session.post(self.api_url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ API call failed: {e}")
            return {"success": False, "error": str(e)}
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode failed: {e}")
            return {"success": False, "error": "Invalid JSON response"}
    
    def calculate_local(self, payload: Dict[str, str]) -> Dict[str, Any]:
        """
        Calculate results using local cal_num
        
        Args:
            payload: Dictionary containing full_name, date_of_birth, current_date
            
        Returns:
            Local calculation results
        """
        try:
            calculator = CalNum(
                dob=payload["date_of_birth"],
                current_date=payload["current_date"],
                name=payload["full_name"]
            )
            return calculator.get_personal_date_num()
        except Exception as e:
            print(f"❌ Local calculation failed: {e}")
            return {"error": str(e)}
    
    def compare_results(self, local_results: Dict[str, Any], api_results: Dict[str, Any]) -> Dict[str, str]:
        """
        Compare local results with API results
        
        Args:
            local_results: Results from local calculation
            api_results: Results from API
            
        Returns:
            Dictionary with comparison status for each field
        """
        comparison = {}
        
        if "pwi_indices" not in api_results:
            return {"error": "API response missing pwi_indices"}
        
        api_indices = api_results["data"]["pwi_indices"]
        
        # Field mapping between local and API
        field_mapping = {
            "life_path": "life_path",
            "life_purpose": "life_purpose", 
            "balance": "balance",
            "soul": "soul",
            "personality": "personality",
            "birth_day": "birth_day",
            "subconscious_strength": "subconscious_strength",
            "maturity": "maturity",
            "missing_aspects": "missing_aspects",
            "shadow_challenge_code": "shadow_challenge_code",
            "passion": "passion",
            "societal_adaptability_index": "societal_adaptability_index",
            "emotional_response_style": "emotional_response_style",
            "link_connection": "link_connection",
            "milestone_phase": "milestone_phase",
            "challenge": "challenge",
            "soul_personality_link": "soul_personality_link",
            "rational_thinking": "rational_thinking",
            "age_milestones": "age_milestones",
            "alignment_signals": "alignment_signals"
        }
        
        for api_key, local_key in field_mapping.items():
            if api_key in api_indices and local_key in local_results:
                local_value = local_results[local_key]
                api_value = api_indices[api_key]
                
                # Debug comparison
                print(f"DEBUG: Comparing {api_key}")
                print(f"  Local: {local_value} (type: {type(local_value)})")
                print(f"  API:   {api_value} (type: {type(api_value)})")
                print(f"  Equal: {local_value == api_value}")
                
                if local_value == api_value:
                    comparison[api_key] = "MATCH"
                else:
                    comparison[api_key] = "MISMATCH"
            else:
                comparison[api_key] = "NOT_FOUND"
        
        return comparison
    
    def format_value(self, value: Any) -> str:
        """Format value for display"""
        if isinstance(value, (list, dict)):
            return str(value)
        return str(value)
    
    def test_single_payload(self, payload: Dict[str, str], test_name: str = "") -> Dict[str, Any]:
        """
        Test a single payload and return detailed results
        
        Args:
            payload: Dictionary containing full_name, date_of_birth, current_date
            test_name: Name for this test case
            
        Returns:
            Dictionary with test results and comparison
        """
        print(f"\n{'='*60}")
        print(f"🧪 TESTING: {test_name or 'Unnamed Test'}")
        print(f"{'='*60}")
        print(f"Payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")
        
        # Call API
        print("\n📡 Calling API...")
        api_response = self.call_api(payload)
        
        if not api_response.get("success"):
            print(f"❌ API call failed: {api_response.get('error', 'Unknown error')}")
            return {"success": False, "error": api_response.get("error")}
        
        print("✅ API call successful")
        
        # Calculate locally
        print("\n🧮 Calculating locally...")
        local_results = self.calculate_local(payload)
        
        if "error" in local_results:
            print(f"❌ Local calculation failed: {local_results['error']}")
            return {"success": False, "error": local_results["error"]}
        
        print("✅ Local calculation successful")
        
        # Compare results
        print("\n🔍 Comparing results...")
        comparison = self.compare_results(local_results, api_response)
        
        # Display comparison
        print("\n📊 COMPARISON RESULTS:")
        print("-" * 50)
        
        api_indices = api_response["data"]["pwi_indices"]
        match_count = 0
        mismatch_count = 0
        not_found_count = 0
        
        # Field mapping between local and API
        field_mapping = {
            "life_path": "life_path",
            "life_purpose": "life_purpose", 
            "balance": "balance",
            "soul": "soul",
            "personality": "personality",
            "birth_day": "birth_day",
            "subconscious_strength": "subconscious_strength",
            "maturity": "maturity",
            "missing_aspects": "missing_aspects",
            "shadow_challenge_code": "shadow_challenge_code",
            "passion": "passion",
            "societal_adaptability_index": "societal_adaptability_index",
            "emotional_response_style": "emotional_response_style",
            "link_connection": "link_connection",
            "milestone_phase": "milestone_phase",
            "challenge": "challenge",
            "soul_personality_link": "soul_personality_link",
            "rational_thinking": "rational_thinking",
            "age_milestones": "age_milestones",
            "alignment_signals": "alignment_signals"
        }
        
        for api_key in api_indices.keys():
            if api_key in field_mapping:
                local_key = field_mapping[api_key]
                if local_key in local_results:
                    local_value = local_results[local_key]
                    api_value = api_indices[api_key]
                    
                    # Check if values match
                    is_match = local_value == api_value
                    
                    if is_match:
                        match_count += 1
                        status_icon = "✅"
                    else:
                        mismatch_count += 1
                        status_icon = "❌"
                    
                    print(f"{status_icon} {api_key:25} | Local: {self.format_value(local_value):15} | API: {self.format_value(api_value):15}")
                else:
                    not_found_count += 1
                    print(f"⚠️ {api_key:25} | Local: {'N/A':15} | API: {self.format_value(api_indices[api_key]):15}")
            else:
                not_found_count += 1
                print(f"⚠️ {api_key:25} | Local: {'N/A':15} | API: {self.format_value(api_indices[api_key]):15}")
        
        # Summary
        total_fields = len(api_indices)
        print(f"\n📈 SUMMARY:")
        print(f"Total fields: {total_fields}")
        print(f"✅ Matches: {match_count}")
        print(f"❌ Mismatches: {mismatch_count}")
        print(f"⚠️  Not found: {not_found_count}")
        print(f"🎯 Accuracy: {(match_count/total_fields)*100:.1f}%")
        
        # Detailed analysis for mismatches
        if mismatch_count > 0:
            print(f"\n🔍 DETAILED ANALYSIS FOR MISMATCHES:")
            print("-" * 50)
            
            for api_key in api_indices.keys():
                if api_key in field_mapping:
                    local_key = field_mapping[api_key]
                    if local_key in local_results:
                        local_value = local_results[local_key]
                        api_value = api_indices[api_key]
                        
                        if local_value != api_value:
                            print(f"\n{api_key}:")
                            print(f"  Local: {local_value}")
                            print(f"  API:   {api_value}")
                            print(f"  Types: Local={type(local_value)}, API={type(api_value)}")
        
        return {
            "success": True,
            "payload": payload,
            "api_response": api_response,
            "local_results": local_results,
            "comparison": comparison,
            "stats": {
                "total": total_fields,
                "matches": match_count,
                "mismatches": mismatch_count,
                "not_found": not_found_count,
                "accuracy": (match_count/total_fields)*100
            }
        }
    
    def run_bulk_tests(self, test_cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Run multiple test cases
        
        Args:
            test_cases: List of test case dictionaries with payload and name
            
        Returns:
            List of test results
        """
        print("🚀 STARTING BULK API TESTS")
        print("=" * 60)
        
        results = []
        
        for i, test_case in enumerate(test_cases, 1):
            payload = test_case["payload"]
            test_name = test_case.get("name", f"Test Case {i}")
            
            print(f"\n📋 Test {i}/{len(test_cases)}: {test_name}")
            
            try:
                result = self.test_single_payload(payload, test_name)
                results.append(result)
                
                # Add delay between API calls to be respectful
                if i < len(test_cases):
                    print("\n⏳ Waiting 2 seconds before next test...")
                    time.sleep(2)
                    
            except Exception as e:
                print(f"❌ Test failed with exception: {e}")
                results.append({
                    "success": False,
                    "payload": payload,
                    "test_name": test_name,
                    "error": str(e)
                })
        
        # Overall summary
        self.print_overall_summary(results)
        
        return results
    
    def print_overall_summary(self, results: List[Dict[str, Any]]):
        """Print overall summary of all test results"""
        print("\n" + "="*60)
        print("🎯 OVERALL TEST SUMMARY")
        print("="*60)
        
        successful_tests = [r for r in results if r.get("success")]
        failed_tests = [r for r in results if not r.get("success")]
        
        print(f"Total tests: {len(results)}")
        print(f"✅ Successful: {len(successful_tests)}")
        print(f"❌ Failed: {len(failed_tests)}")
        
        if successful_tests:
            total_accuracy = sum(r["stats"]["accuracy"] for r in successful_tests)
            avg_accuracy = total_accuracy / len(successful_tests)
            print(f"🎯 Average accuracy: {avg_accuracy:.1f}%")
            
            perfect_tests = [r for r in successful_tests if r["stats"]["accuracy"] == 100.0]
            print(f"🏆 Perfect matches: {len(perfect_tests)}/{len(successful_tests)}")
        
        # Test case details
        print(f"\n📋 TEST CASE DETAILS:")
        for i, result in enumerate(results, 1):
            if result.get("success"):
                stats = result["stats"]
                test_name = result.get("test_name", f"Test {i}")
                print(f"  {i}. {test_name}: {stats['accuracy']:.1f}% ({stats['matches']}/{stats['total']})")
            else:
                test_name = result.get("test_name", f"Test {i}")
                print(f"  {i}. {test_name}: ❌ FAILED")


def main():
    """Main function to run bulk tests"""
    
    # Test cases with different names and dates
    test_cases = [
        {
            "name": "Vietnamese Name 1 - Huỳnh Đăng Nghĩa",
            "payload": {
                "full_name": "Huỳnh Đăng Nghĩa",
                "date_of_birth": "27/10/2002",
                "current_date": "07/08/2025"
            }
        },
        {
            "name": "Vietnamese Name 2 - Nguyễn Hữu Thành Trung",
            "payload": {
                "full_name": "Nguyễn Hữu Thành Trung",
                "date_of_birth": "03/01/2003",
                "current_date": "15/08/2025"
            }
        },
        {
            "name": "Vietnamese Name 3 - Trần Thị Mai Anh",
            "payload": {
                "full_name": "Trần Thị Mai Anh",
                "date_of_birth": "15/06/1995",
                "current_date": "20/12/2024"
            }
        }
    ]
    
    # Create tester and run tests
    tester = BulkAPITester()
    results = tester.run_bulk_tests(test_cases)
    
    # Save results to file
    output_file = "bulk_test_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    return results


if __name__ == "__main__":
    main()
