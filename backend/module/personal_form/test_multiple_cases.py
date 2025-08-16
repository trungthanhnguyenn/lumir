#!/usr/bin/env python3
"""
Test script with multiple cases to verify Y vowel logic
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cal_num import CalNum

def test_multiple_cases():
    """Test multiple cases with Y vowel logic"""
    
    test_cases = [
        {
            "name": "Nguyễn Diệu Lý",
            "expected_soul": 5,
            "description": "Y in Lý should be vowel (only vowel in word)"
        },
        {
            "name": "Nguyễn Thy",
            "expected_soul": 6,  # Updated: 8 + 7 = 15 -> 6
            "description": "Y in Thy should be vowel (only vowel in word)"
        },
        {
            "name": "Lý Văn",
            "expected_soul": 8,
            "description": "Y in Lý should be vowel"
        },
        {
            "name": "Nguyễn Vy",
            "expected_soul": 6,  # Updated: 8 + 7 = 15 -> 6
            "description": "Y in Vy should be vowel (only vowel in word)"
        },
        {
            "name": "Diệu Yến",
            "expected_soul": 4,  # Updated: 8 + 5 = 13 -> 4
            "description": "Y in Yến should be consonant (has ế)"
        }
    ]
    
    print("🧪 TESTING MULTIPLE CASES WITH Y VOWEL LOGIC")
    print("=" * 60)
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i}: {case['name']} ---")
        print(f"Description: {case['description']}")
        
        calculator = CalNum("15/06/1995", "20/12/2024", case["name"])
        name_parts = calculator._split_name_parts()
        
        print(f"Name parts: {name_parts}")
        
        # Analyze each part
        total_soul_sum = 0
        for part in name_parts:
            vowels = []
            vowel_numbers = []
            
            for char in part:
                if calculator._is_vowel(char, part):  # Pass current_word
                    vowels.append(char)
                    number = calculator.ALPHABET.get(char.upper(), 0)
                    vowel_numbers.append(number)
            
            part_vowel_sum = sum(vowel_numbers)
            reduced = calculator.reduce_number_with_masters(part_vowel_sum)
            
            print(f"  '{part}': vowels={vowels}, numbers={vowel_numbers}, sum={part_vowel_sum}, reduced={reduced}")
            total_soul_sum += reduced
        
        final_soul = calculator.reduce_number_with_masters(total_soul_sum)
        expected = case["expected_soul"]
        
        print(f"Total soul sum: {total_soul_sum}")
        print(f"Final soul: {final_soul}")
        print(f"Expected: {expected}")
        print(f"✅ Match: {final_soul == expected}")
        
        if final_soul != expected:
            print(f"❌ MISMATCH! Expected {expected}, got {final_soul}")

if __name__ == "__main__":
    test_multiple_cases()
