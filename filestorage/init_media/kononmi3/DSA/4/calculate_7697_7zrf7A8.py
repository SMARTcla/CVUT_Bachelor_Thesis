import re

def count_consonants(s):
    pattern = r'[b-df-hj-np-tv-z]'
    matches = re.findall(pattern, s, flags=re.IGNORECASE)
    return len(matches)