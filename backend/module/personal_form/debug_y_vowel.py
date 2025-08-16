#!/usr/bin/env python3
"""
Debug script to check Y vowel logic
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cal_num import CalNum

def debug_y_vowel():
    """Debug Y vowel logic"""
    
    test_names = ["Nguyễn Diệu Lý", "Nguyễn Thy", "Nguyễn Vy"]
    
    for name in test_names:
        print(f"\n{'='*60}")
        print(f"DEBUGGING: {name}")
        print(f"{'='*60}")
        
        calculator = CalNum("15/06/1995", "20/12/2024", name)
        name_parts = calculator._split_name_parts()
        print(f"Name parts: {name_parts}")
        
        # Analyze each part for soul calculation
        print(f"\n🔍 SOUL CALCULATION ANALYSIS:")
        print("-" * 30)
        
        total_soul_sum = 0
        
        for part in name_parts:
            print(f"\nPart: '{part}'")
            
            # Find vowels in this part
            vowels = []
            vowel_numbers = []
            
            for char in part:
                is_vowel = calculator._is_vowel(char, part)
                if is_vowel:
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

if __name__ == "__main__":
    debug_y_vowel()
