#!/usr/bin/env python3
"""
Test script to verify the fixes for balance, rational_thinking, and name validation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cal_num import CalNum

def test_fixes():
    """Test the fixes for balance, rational_thinking, and name validation"""
    
    print("🧪 TESTING FIXES")
    print("=" * 60)
    
    # Test case 1: Normal name with 4 parts
    print("\n--- Test Case 1: Nguyễn Hữu Thành Trung ---")
    calculator1 = CalNum("03/01/2003", "Nguyễn Hữu Thành Trung")
    
    print(f"Name parts: {calculator1._split_name_parts()}")
    print(f"First letters: N, H, T, T")
    print(f"First letter values: {calculator1.ALPHABET['N']}, {calculator1.ALPHABET['H']}, {calculator1.ALPHABET['T']}, {calculator1.ALPHABET['T']}")
    
    balance1 = calculator1.calculate_balance()
    print(f"Balance calculation: {calculator1.ALPHABET['N']} + {calculator1.ALPHABET['H']} + {calculator1.ALPHABET['T']} + {calculator1.ALPHABET['T']} = {calculator1.ALPHABET['N'] + calculator1.ALPHABET['H'] + calculator1.ALPHABET['T'] + calculator1.ALPHABET['T']}")
    print(f"Balance result: {balance1}")
    
    rational1 = calculator1.calculate_rational_thinking()
    print(f"Rational thinking: day({calculator1.day}) + sum(given_name 'Trung') = {calculator1.day} + {sum(calculator1.ALPHABET.get(char.upper(), 0) for char in 'Trung' if char.upper() in calculator1.ALPHABET)}")
    print(f"Rational thinking result: {rational1}")
    
    # Test case 2: Short name with 2 parts
    print("\n--- Test Case 2: Lý Văn ---")
    calculator2 = CalNum("15/06/1995", "Lý Văn")
    
    print(f"Name parts: {calculator2._split_name_parts()}")
    print(f"First letters: L, V")
    print(f"First letter values: {calculator2.ALPHABET['L']}, {calculator2.ALPHABET['V']}")
    
    balance2 = calculator2.calculate_balance()
    print(f"Balance calculation: {calculator2.ALPHABET['L']} + {calculator2.ALPHABET['V']} = {calculator2.ALPHABET['L'] + calculator2.ALPHABET['V']}")
    print(f"Balance result: {balance2}")
    
    rational2 = calculator2.calculate_rational_thinking()
    print(f"Rational thinking: day({calculator2.day}) + sum(given_name 'Văn') = {calculator2.day} + {sum(calculator2.ALPHABET.get(char.upper(), 0) for char in 'Văn' if char.upper() in calculator2.ALPHABET)}")
    print(f"Rational thinking result: {rational2}")
    
    # Test case 3: Single name
    print("\n--- Test Case 3: Nguyễn ---")
    calculator3 = CalNum("15/06/1995", "Nguyễn")
    
    print(f"Name parts: {calculator3._split_name_parts()}")
    print(f"First letters: N")
    print(f"First letter values: {calculator3.ALPHABET['N']}")
    
    balance3 = calculator3.calculate_balance()
    print(f"Balance calculation: {calculator3.ALPHABET['N']}")
    print(f"Balance result: {balance3}")
    
    rational3 = calculator3.calculate_rational_thinking()
    print(f"Rational thinking: day({calculator3.day}) + sum(given_name 'Nguyễn') = {calculator3.day} + {sum(calculator3.ALPHABET.get(char.upper(), 0) for char in 'Nguyễn' if char.upper() in calculator3.ALPHABET)}")
    print(f"Rational thinking result: {rational3}")
    
    # Test case 4: Test master number preservation in rational_thinking
    print("\n--- Test Case 4: Test Master Number Preservation ---")
    # Create a case where day + given_name_sum might result in a master number
    calculator4 = CalNum("11/06/1995", "A B")  # day=11, very short names
    
    rational4 = calculator4.calculate_rational_thinking()
    print(f"Rational thinking: day({calculator4.day}) + sum(given_name 'B') = {calculator4.day} + {sum(calculator4.ALPHABET.get(char.upper(), 0) for char in 'B' if char.upper() in calculator4.ALPHABET)}")
    print(f"Rational thinking result: {rational4}")
    print(f"Is master number preserved: {rational4 in calculator4.MASTER_NUMBERS}")

if __name__ == "__main__":
    test_fixes()
