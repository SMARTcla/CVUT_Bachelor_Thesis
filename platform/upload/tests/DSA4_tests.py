def run_tests(student_module):
    """
    Executes the tests for the count_consonants(s) function.
    Returns a tuple (bool, str) indicating success and a message.
    """
    try:
        if not hasattr(student_module, 'count_consonants'):
            return False, "Function 'count_consonants' not found."

        test_cases = [
            {'s': 'hello', 'expected': 3},
            {'s': 'Django', 'expected': 4},
            {'s': 'AEIOU', 'expected': 0},
            {'s': 'bcdfghjklmnpqrstvwxyz', 'expected': 21},
            {'s': 'Python Programming', 'expected': 13},
            {'s': '', 'expected': 0},
            {'s': '12345', 'expected': 0},
            {'s': 'Consonants!', 'expected': 7},
            {'s': 'This is a test string.', 'expected': 12},
            {'s': 'D3v3l0p3r', 'expected': 5},
        ]

        passed_tests = 0
        failed_tests = []
        for i, test in enumerate(test_cases, start=1):
            a = test['s']
            expected = test['expected']
            try:
                result = student_module.count_consonants(a)
                if result == expected:
                    passed_tests += 1
                else:
                    failed_tests.append(f"Test {i}: count_consonants({a}) returned {result}, expected {expected}.")
            except Exception as e:
                failed_tests.append(f"Test {i}: Raised an exception: {e}.")

        total_tests = len(test_cases)
        if passed_tests == total_tests:
            return (passed_tests, total_tests, "All tests passed successfully.")
        else:
            return (passed_tests, total_tests, " ".join(failed_tests))

    except Exception as e:
        return (0, 10, f"Error during execution: {e}")

