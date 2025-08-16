#!/usr/bin/env python3
"""
Debug script to check comparison logic
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cal_num import CalNum
import json

def debug_comparison():
    """Debug the comparison logic"""
    
    # Test data
    payload = {
        "full_name": "Huỳnh Đăng Nghĩa",
        "date_of_birth": "27/10/2002",
        "current_date": "07/08/2025"
    }
    
    print("🔍 DEBUG COMPARISON LOGIC")
    print("=" * 50)
    
    # Get local results
    calculator = CalNum(
        dob=payload["date_of_birth"],
        current_date=payload["current_date"],
        name=payload["full_name"]
    )
    local_results = calculator.get_personal_date_num()
    
    print("Local results keys:")
    for key in local_results.keys():
        print(f"  - {key}: {local_results[key]}")
    
    print("\n" + "=" * 50)
    
    # Mock API response structure
    api_response = {
        "success": True,
        "data": {
            "pwi_indices": {
                "life_path": 5,
                "life_purpose": 6,
                "balance": 8,
                "soul": 5,
                "personality": 1,
                "birth_day": 9,
                "subconscious_strength": 7,
                "maturity": 11,
                "missing_aspects": [2, 6],
                "shadow_challenge_code": "Có Karmic Debt",
                "passion": [8, 7, 5],
                "societal_adaptability_index": "Gen Z - Công nghệ số, đa dạng, thay đổi nhanh",
                "emotional_response_style": 5,
                "link_connection": 4,
                "milestone_phase": {
                    "milestone_1": 1,
                    "milestone_2": 4,
                    "milestone_3": 5,
                    "milestone_4": 5
                },
                "challenge": {
                    "challenge_1": 8,
                    "challenge_2": 5,
                    "challenge_3": 3,
                    "challenge_4": 3
                },
                "soul_personality_link": 4,
                "rational_thinking": 3,
                "age_milestones": [31, 40, 49, 58],
                "alignment_signals": {
                    "personal_year": 1,
                    "personal_day": 7
                }
            }
        }
    }
    
    print("API response structure:")
    print(f"API keys: {list(api_response['data']['pwi_indices'].keys())}")
    
    print("\n" + "=" * 50)
    
    # Test comparison logic
    api_indices = api_response["data"]["pwi_indices"]
    
    # Field mapping
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
    
    print("Testing field mapping:")
    for api_key, local_key in field_mapping.items():
        api_exists = api_key in api_indices
        local_exists = local_key in local_results
        
        print(f"\n{api_key}:")
        print(f"  API exists: {api_exists}")
        print(f"  Local exists: {local_exists}")
        
        if api_exists and local_exists:
            local_value = local_results[local_key]
            api_value = api_indices[api_key]
            is_match = local_value == api_value
            
            print(f"  Local value: {local_value}")
            print(f"  API value: {api_value}")
            print(f"  Match: {is_match}")
            
            if not is_match:
                print(f"  Type comparison:")
                print(f"    Local type: {type(local_value)}")
                print(f"    API type: {type(api_value)}")
                print(f"    Local == API: {local_value == api_value}")
                print(f"    Local is API: {local_value is api_value}")

if __name__ == "__main__":
    debug_comparison()
