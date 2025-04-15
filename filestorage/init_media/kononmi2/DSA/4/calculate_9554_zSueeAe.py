def count_consonants(s):
    vowels = "aeiou"
    consonant_total = sum(1 for char in s if char.isalpha() and char.lower() not in vowels)
    return consonant_total