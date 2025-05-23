import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'software_app.settings')
django.setup()

from upload.models import Subject, Assignment

def populate():
    subjects = {
        'PDA': 'Principles of Distributed Applications',
        'DSA': 'Data Structures and Algorithms',
        'OMO': 'Object-Oriented Modeling',
        'NSS': 'Network Security Systems',
    }

    assignments = {
        'PDA': [
            {
                'name': 'Homework 1',
                'description': (
                    "📄 **File Name:** `calculate.py`\n\n"
                    "🛠 **Main Function:** `calculate(a, b)`\n\n"
                    "✏️ **Task:** Write a function `calculate(a, b)` that returns the sum of two numbers `a` and `b`.\n\n"
                    "🔍 **Example Outputs:**\n"
                    "- `calculate(2, 3)` should return `5`\n"
                    "- `calculate(-1, 1)` should return `0`\n"
                    "- `calculate(0, 0)` should return `0`"
                ),
                'deadline': date.today() + timedelta(days=7), 
                'number': 5
            },
        ],
        'DSA': [
            {
                'name': 'Homework 1',
                'description': (
                    "📄 **File Name:** `calculate.py`\n\n"
                    "🛠 **Main Function:** `calculate(a, b)`\n\n"
                    "✏️ **Task:** Write a function `calculate(a, b)` that returns the sum of two numbers `a` and `b`.\n\n"
                    "🔍 **Example Outputs:**\n"
                    "- `calculate(2, 3)` should return `5`\n"
                    "- `calculate(-1, 1)` should return `0`\n"
                    "- `calculate(0, 0)` should return `0`"
                ),
                'deadline': date.today() + timedelta(days=5), 
                'number': 1
            },
            {
                'name': 'Homework 2',
                'description': (
                    "📄 **File Name:** `calculate.py`\n\n"
                    "🛠 **Main Function:** `pow_cal(a, b)`\n\n"
                    "✏️ **Task:** Write a function `pow_cal(a, b)` that calculates `a` raised to the power of `b` (i.e., `a ** b`).\n\n"
                    "🔍 **Example Outputs:**\n"
                    "- `pow_cal(2, 3)` should return `8`\n"
                    "- `pow_cal(-1, 2)` should return `1`\n"
                    "- `pow_cal(0, 0)` should return `1` (Note: `0**0` is mathematically undefined; handle as per your requirements)"
                ),
                'deadline': date.today() + timedelta(days=12), 
                'number': 2
            },
            {
                'name': 'Homework 3',
                'description': (
                    "📄 **File Name:** `calculate.py`\n\n"
                    "🛠 **Main Function:** `len_arr(arr)`\n\n"
                    "✏️ **Task:** Write a function `len_arr(arr)` that takes an array `arr` as input and returns its length.\n\n"
                    "🔍 **Example Outputs:**\n"
                    "- `len_arr([1, 2, 3])` should return `3`\n"
                    "- `len_arr([])` should return `0`\n"
                    "- `len_arr(['a', 'b'])` should return `2`"
                ),
                'deadline': date.today() + timedelta(days=19), 
                'number': 3
            },
            {
                'name': 'Homework 4',
                'description': (
                    "📄 **File Name:** `calculate.py`\n\n"
                    "🛠 **Main Function:** `count_consonants(s)`\n\n"
                    "✏️ **Task:** Write a function `count_consonants(s)` that takes a string `s` as input and returns the count of consonant letters in the string.\n\n"
                    "🔍 **Example Outputs:**\n"
                    "- `count_consonants('hello')` should return `3`\n"
                    "- `count_consonants('Django')` should return `3`\n"
                    "- `count_consonants('AEIOU')` should return `0`"
                ),
                'deadline': date.today() + timedelta(days=26), 
                'number': 4
            },
        ],
        'OMO': [
        ],
        'NSS': [
        ],
    }

    for subject_abbr, subject_desc in subjects.items():
        subject, created = Subject.objects.get_or_create(name=subject_abbr, defaults={'description': subject_desc})
        if created:
            print(f"Created subject: {subject_abbr}")
        else:
            print(f"Subject already exists: {subject_abbr}")

        for assignment_data in assignments.get(subject_abbr, []):
            assignment, created = Assignment.objects.get_or_create(
                subject=subject,
                name=assignment_data['name'],
                defaults={
                    'description': assignment_data['description'],
                    'deadline': assignment_data['deadline'],
                    'number': assignment_data['number'],
                }
            )
            if created:
                print(f"  Created assignment: {assignment.name} (Number: {assignment.number})")
            else:
                print(f"  Assignment already exists: {assignment.name} (Number: {assignment.number})")

if __name__ == '__main__':
    populate()
