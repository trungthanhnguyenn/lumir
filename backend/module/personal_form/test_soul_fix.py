#!/usr/bin/env python3
"""
Test script to check soul number calculation with "Nguyễn Diệu Lý"
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cal_num import CalNum

def test_soul_calculation():
    """Test soul number calculation with Nguyễn Diệu Lý"""
    
    # Test data
    name = "Nguyễn Diệu Lý"
    dob = "15/06/1995"
    current_date = "20/12/2024"
    
    print("🧪 TESTING SOUL NUMBER CALCULATION")
    print("=" * 50)
    print(f"Name: {name}")
    print(f"DOB: {dob}")
    print(f"Current Date: {current_date}")
    print("=" * 50)
    
    # Create calculator
    calculator = CalNum(dob, current_date, name)
    
    # Get name parts
    name_parts = calculator._split_name_parts()
    print(f"\nName parts: {name_parts}")
    
    # Analyze each part for soul calculation
    print("\n🔍 SOUL CALCULATION ANALYSIS:")
    print("-" * 30)
    
    total_soul_sum = 0
    
    for part in name_parts:
        print(f"\nPart: '{part}'")
        
        # Find vowels in this part
        vowels = []
        vowel_numbers = []
        
        for char in part:
            if calculator._is_vowel(char):
                vowels.append(char)
                number = calculator.ALPHABET.get(char.upper(), 0)
                vowel_numbers.append(number)
        
        part_vowel_sum = sum(vowel_numbers)
        reduced = calculator.reduce_number_with_masters(part_vowel_sum)
        
        print(f"  Vowels: {vowels}")
        print(f"  Vowel numbers: {vowel_numbers}")
        print(f"  Sum: {part_vowel_sum}")
        print(f"  Reduced: {reduced}")
        
        total_soul_sum += reduced
    
    # Final soul calculation
    final_soul = calculator.reduce_number_with_masters(total_soul_sum)
    
    print(f"\n📊 FINAL SOUL CALCULATION:")
    print(f"Total soul sum: {total_soul_sum}")
    print(f"Final soul: {final_soul}")
    
    # Expected result
    expected_soul = 5
    print(f"\n🎯 EXPECTED: {expected_soul}")
    print(f"✅ ACTUAL: {final_soul}")
    print(f"🎯 MATCH: {final_soul == expected_soul}")
    
    # Character by character analysis
    print(f"\n🔤 CHARACTER BY CHARACTER ANALYSIS:")
    print("-" * 40)
    
    name_parts = calculator._split_name_parts()
    current_pos = 0
    
    for part in name_parts:
        for i, char in enumerate(part):
            number = calculator.ALPHABET.get(char.upper(), 0)
            is_vowel = calculator._is_vowel(char, part)
            is_consonant = calculator._is_consonant(char, part)
            print(f"  {current_pos + i + 1:2d}. '{char}' → {number:2d} | Vowel: {is_vowel} | Consonant: {is_consonant}")
        current_pos += len(part)
    
    return final_soul == expected_soul

if __name__ == "__main__":
    success = test_soul_calculation()
    if success:
        print("\n🎉 SUCCESS: Soul number calculation is correct!")
    else:
        print("\n❌ FAILED: Soul number calculation needs fixing!")
