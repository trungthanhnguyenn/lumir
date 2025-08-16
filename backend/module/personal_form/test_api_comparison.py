#!/usr/bin/env python3
"""
Test script to compare local calculation results with API response
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cal_num import CalNum
import json

def format_value(value):
    """Format value for display"""
    if isinstance(value, (list, dict)):
        return str(value)
    return str(value)

def test_api_comparison():
    """Test and compare local calculation with API response"""
    
    # Input data from API
    input_data = {
        "full_name": "Nguyễn Hữu Thành Trung",
        "date_of_birth": "03/01/2003",
        "current_date": "15/08/2025"
    }
    
    # API response for comparison
    api_response = {
        "success": True,
        "data": {
            "input": input_data,
            "pwi_indices": {
                "life_path": 9,
                "life_purpose": 6,
                "balance": 6,
                "soul": 9,
                "personality": 6,
                "birth_day": 3,
                "subconscious_strength": 7,
                "maturity": 6,
                "missing_aspects": [4, 6],
                "shadow_challenge_code": "Không có Karmic Debt",
                "passion": [5],
                "societal_adaptability_index": "Gen Z - Công nghệ số, đa dạng, thay đổi nhanh",
                "emotional_response_style": 22,
                "link_connection": 3,
                "milestone_phase": {
                    "milestone_1": 4,
                    "milestone_2": 8,
                    "milestone_3": 3,
                    "milestone_4": 6
                },
                "challenge": {
                    "challenge_1": 2,
                    "challenge_2": 2,
                    "challenge_3": 0,
                    "challenge_4": 4
                },
                "soul_personality_link": 3,
                "rational_thinking": 2,
                "age_milestones": [27, 36, 45, 54],
                "alignment_signals": {
                    "personal_year": 4,
                    "personal_day": 9
                }
            }
        }
    }
    
    print("🔍 Testing API Comparison")
    print("=" * 50)
    print(f"Input: {input_data['full_name']} - {input_data['date_of_birth']} - {input_data['current_date']}")
    print("=" * 50)
    
    # Create calculator instance
    try:
        calculator = CalNum(
            dob=input_data["date_of_birth"],
            current_date=input_data["current_date"],
            name=input_data["full_name"]
        )
        print("✅ Calculator initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing calculator: {e}")
        return
    
    # Get local results
    local_results = calculator.get_personal_date_num()
    
    # Get API results
    api_results = api_response["data"]["pwi_indices"]
    
    # Compare results
    print("\n📊 COMPARISON RESULTS:")
    print("=" * 50)
    
    comparison_results = {}
    
    for key in api_results.keys():
        if key in local_results:
            local_value = local_results[key]
            api_value = api_results[key]
            
            if local_value == api_value:
                status = "✅ MATCH"
                comparison_results[key] = "MATCH"
            else:
                status = "❌ MISMATCH"
                comparison_results[key] = "MISMATCH"
            
            print(f"{key:25} | Local: {format_value(local_value):15} | API: {format_value(api_value):15} | {status}")
        else:
            print(f"{key:25} | Local: {'N/A':15} | API: {format_value(api_results[key]):15} | ⚠️  NOT FOUND")
            comparison_results[key] = "NOT_FOUND"
    
    # Summary
    print("\n📈 SUMMARY:")
    print("=" * 50)
    
    match_count = sum(1 for v in comparison_results.values() if v == "MATCH")
    mismatch_count = sum(1 for v in comparison_results.values() if v == "MISMATCH")
    not_found_count = sum(1 for v in comparison_results.values() if v == "NOT_FOUND")
    
    print(f"Total fields: {len(comparison_results)}")
    print(f"✅ Matches: {match_count}")
    print(f"❌ Mismatches: {mismatch_count}")
    print(f"⚠️  Not found: {not_found_count}")
    
    # Detailed analysis for mismatches
    if mismatch_count > 0:
        print("\n🔍 DETAILED ANALYSIS FOR MISMATCHES:")
        print("=" * 50)
        
        for key in api_results.keys():
            if key in local_results:
                local_value = local_results[key]
                api_value = api_results[key]
                
                if local_value != api_value:
                    print(f"\n{key}:")
                    print(f"  Local: {local_value}")
                    print(f"  API:   {api_value}")
                    
                    # Show calculation details for some fields
                    if key == "life_path":
                        print(f"  Calculation: day_r({calculator.day_r}) + month_r({calculator.month_r}) + year_r({calculator.year_r}) = {calculator.day_r + calculator.month_r + calculator.year_r}")
                        print(f"  Reduced: {calculator.reduce_number_with_masters(calculator.day_r + calculator.month_r + calculator.year_r)}")
                    
                    elif key == "life_purpose":
                        print(f"  Name numbers: {calculator.name_numbers}")
                        print(f"  Name sum: {sum(calculator.name_numbers)}")
                        print(f"  Reduced: {calculator.reduce_number(sum(calculator.name_numbers))}")
                    
                    elif key == "soul":
                        name_parts = calculator._split_name_parts()
                        print(f"  Name parts: {name_parts}")
                        for part in name_parts:
                            vowels = [char for char in part if calculator._is_vowel(char)]
                            vowel_sum = sum(calculator.ALPHABET.get(char.upper(), 0) for char in vowels)
                            print(f"    '{part}': vowels={vowels}, sum={vowel_sum}, reduced={calculator.reduce_number_with_masters(vowel_sum)}")
                    
                    elif key == "personality":
                        name_parts = calculator._split_name_parts()
                        print(f"  Name parts: {name_parts}")
                        for part in name_parts:
                            consonants = [char for char in part if calculator._is_consonant(char)]
                            consonant_sum = sum(calculator.ALPHABET.get(char.upper(), 0) for char in consonants)
                            print(f"    '{part}': consonants={consonants}, sum={consonant_sum}, reduced={calculator.reduce_number_with_masters(consonant_sum)}")
                    
                    elif key == "subconscious_strength":
                        missing_aspects = calculator.get_missing_aspects()
                        print(f"  Missing aspects: {missing_aspects}")
                        print(f"  Count: {len(missing_aspects)}")
                        print(f"  Result: 9 - {len(missing_aspects)} = {9 - len(missing_aspects)}")
    
    # Show name analysis
    print("\n🔤 NAME ANALYSIS:")
    print("=" * 50)
    print(f"Original name: '{input_data['full_name']}'")
    print(f"Clean name: '{''.join(input_data['full_name'].upper().split())}'")
    print(f"Name parts: {calculator._split_name_parts()}")
    print(f"Name numbers: {calculator.name_numbers}")
    print(f"Name sum: {sum(calculator.name_numbers)}")
    
    # Show date analysis
    print("\n📅 DATE ANALYSIS:")
    print("=" * 50)
    print(f"Day: {calculator.day} -> reduced: {calculator.day_r}")
    print(f"Month: {calculator.month} -> reduced: {calculator.month_r}")
    print(f"Year: {calculator.year} -> reduced: {calculator.year_r}")
    print(f"Current date: {calculator.current_datetime.strftime('%d/%m/%Y')}")
    
    return comparison_results

if __name__ == "__main__":
    test_api_comparison()
