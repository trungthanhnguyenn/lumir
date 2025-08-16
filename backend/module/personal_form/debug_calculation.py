#!/usr/bin/env python3
"""
Debug script to analyze calculation details
"""

from cal_num import CalNum

def debug_calculation():
    """Debug calculation details step by step"""
    
    # Test data
    name = "Nguyễn Hữu Thành Trung"
    dob = "03/01/2003"
    current_date = "15/08/2025"
    
    print("🔍 DEBUG CALCULATION DETAILS")
    print("=" * 60)
    print(f"Name: {name}")
    print(f"DOB: {dob}")
    print(f"Current Date: {current_date}")
    print("=" * 60)
    
    # Create calculator
    calculator = CalNum(dob, current_date, name)
    
    # 1. Name Analysis
    print("\n1️⃣ NAME ANALYSIS:")
    print("-" * 30)
    print(f"Original name: '{name}'")
    print(f"Clean name: '{''.join(name.upper().split())}'")
    
    name_parts = calculator._split_name_parts()
    print(f"Name parts: {name_parts}")
    
    print("\nCharacter by character analysis:")
    clean_name = ''.join(name.upper().split())
    for i, char in enumerate(clean_name):
        number = calculator.ALPHABET.get(char, 0)
        is_vowel = calculator._is_vowel(char)
        is_consonant = calculator._is_consonant(char)
        print(f"  {i+1:2d}. '{char}' → {number:2d} | Vowel: {is_vowel} | Consonant: {is_consonant}")
    
    print(f"\nName numbers: {calculator.name_numbers}")
    print(f"Name sum: {sum(calculator.name_numbers)}")
    
    # 2. Date Analysis
    print("\n2️⃣ DATE ANALYSIS:")
    print("-" * 30)
    print(f"Day: {calculator.day} → reduced: {calculator.day_r}")
    print(f"Month: {calculator.month} → reduced: {calculator.month_r}")
    print(f"Year: {calculator.year} → reduced: {calculator.year_r}")
    
    # 3. Life Path Calculation
    print("\n3️⃣ LIFE PATH CALCULATION:")
    print("-" * 30)
    day_r = calculator.day_r
    month_r = calculator.month_r
    year_r = calculator.year_r
    total = day_r + month_r + year_r
    life_path = calculator.reduce_number_with_masters(total)
    print(f"day_r: {day_r}")
    print(f"month_r: {month_r}")
    print(f"year_r: {year_r}")
    print(f"Total: {day_r} + {month_r} + {year_r} = {total}")
    print(f"Reduced: {total} → {life_path}")
    
    # 4. Life Purpose Calculation
    print("\n4️⃣ LIFE PURPOSE CALCULATION:")
    print("-" * 30)
    name_sum = sum(calculator.name_numbers)
    life_purpose = calculator.reduce_number(name_sum)
    print(f"Name sum: {name_sum}")
    print(f"Reduced: {name_sum} → {life_purpose}")
    
    # 5. Soul Calculation
    print("\n5️⃣ SOUL CALCULATION:")
    print("-" * 30)
    for part in name_parts:
        vowels = [char for char in part if calculator._is_vowel(char)]
        vowel_numbers = [calculator.ALPHABET.get(char.upper(), 0) for char in vowels]
        vowel_sum = sum(vowel_numbers)
        reduced = calculator.reduce_number_with_masters(vowel_sum)
        print(f"  '{part}': vowels={vowels} → numbers={vowel_numbers} → sum={vowel_sum} → reduced={reduced}")
    
    soul = calculator.calculate_soul()
    print(f"Final soul: {soul}")
    
    # 6. Personality Calculation
    print("\n6️⃣ PERSONALITY CALCULATION:")
    print("-" * 30)
    for part in name_parts:
        consonants = [char for char in part if calculator._is_consonant(char)]
        consonant_numbers = [calculator.ALPHABET.get(char.upper(), 0) for char in consonants]
        consonant_sum = sum(consonant_numbers)
        reduced = calculator.reduce_number_with_masters(consonant_sum)
        print(f"  '{part}': consonants={consonants} → numbers={consonant_numbers} → sum={consonant_sum} → reduced={reduced}")
    
    personality = calculator.calculate_personality()
    print(f"Final personality: {personality}")
    
    # 7. Missing Aspects
    print("\n7️⃣ MISSING ASPECTS:")
    print("-" * 30)
    name_digits = set()
    for num in calculator.name_numbers:
        for digit in str(num):
            if digit.isdigit():
                name_digits.add(int(digit))
    
    print(f"Digits in name numbers: {sorted(name_digits)}")
    missing = set(range(1, 10)) - name_digits
    print(f"Missing aspects: {sorted(missing)}")
    print(f"Count: {len(missing)}")
    print(f"Subconscious strength: 9 - {len(missing)} = {9 - len(missing)}")
    
    # 8. Passion Calculation
    print("\n8️⃣ PASSION CALCULATION:")
    print("-" * 30)
    from collections import Counter
    digit_counts = Counter()
    for num in calculator.name_numbers:
        for digit in str(num):
            if digit.isdigit():
                digit_counts[int(digit)] += 1
    
    print(f"Digit counts: {dict(digit_counts)}")
    if digit_counts:
        max_freq = max(digit_counts.values())
        passion = [num for num, freq in digit_counts.items() if freq == max_freq]
        print(f"Max frequency: {max_freq}")
        print(f"Passion numbers: {passion}")
    
    # 9. Emotional Response Style
    print("\n9️⃣ EMOTIONAL RESPONSE STYLE:")
    print("-" * 30)
    clean_name = ''.join(name.upper().split())
    first_4 = clean_name[:4]
    first_4_numbers = [calculator.ALPHABET.get(char, 0) for char in first_4]
    first_4_sum = sum(first_4_numbers)
    emotional = calculator.reduce_number(first_4_sum)
    print(f"First 4 characters: '{first_4}'")
    print(f"Numbers: {first_4_numbers}")
    print(f"Sum: {first_4_sum}")
    print(f"Reduced: {first_4_sum} → {emotional}")
    
    # 10. Link Connection
    print("\n🔟 LINK CONNECTION:")
    print("-" * 30)
    soul = calculator.calculate_soul()
    personality = calculator.calculate_personality()
    diff = abs(soul - personality)
    link_connection = calculator.reduce_number(diff)
    soul_personality_link = calculator.reduce_to_single_digit(diff)
    print(f"Soul: {soul}")
    print(f"Personality: {personality}")
    print(f"Difference: |{soul} - {personality}| = {diff}")
    print(f"Link connection: {diff} → {link_connection}")
    print(f"Soul-personality link: {diff} → {soul_personality_link}")

if __name__ == "__main__":
    debug_calculation()
