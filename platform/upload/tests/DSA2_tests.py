def run_tests(student_module):
    """
    Executes the tests for the pow_cal(a, b) function.
    Returns a tuple (passed_tests, total_tests, message).
    """
    try:
        if not hasattr(student_module, 'pow_cal'):
            return (0, 10, "Function 'pow_cal' not found.")

        test_cases = [
            {'a': 2, 'b': 3, 'expected': 8},
            {'a': -1, 'b': 2, 'expected': 1},
            {'a': 0, 'b': 0, 'expected': 1},
            {'a': 5, 'b': 4, 'expected': 625},
            {'a': 10, 'b': 3, 'expected': 1000},
            {'a': 3, 'b': 3, 'expected': 27},
            {'a': -2, 'b': 3, 'expected': -8},
            {'a': 7, 'b': 0, 'expected': 1},
            {'a': 1.5, 'b': 2, 'expected': 2.25},
            {'a': -1.5, 'b': 2, 'expected': 2.25},
        ]

        passed_tests = 0
        failed_tests = []
        for i, test in enumerate(test_cases, start=1):
            a = test['a']
            b = test['b']
            expected = test['expected']
            try:
                result = student_module.pow_cal(a, b)
                if result == expected:
                    passed_tests += 1
                else:
                    failed_tests.append(f"Test {i}: pow_cal({a}, {b}) returned {result}, expected {expected}.")
            except Exception as e:
                failed_tests.append(f"Test {i}: Raised an exception: {e}.")

        total_tests = len(test_cases)
        if passed_tests == total_tests:
            return (passed_tests, total_tests, "All tests passed successfully.")
        else:
            return (passed_tests, total_tests, " ".join(failed_tests))

    except Exception as e:
        return (0, 10, f"Error during execution: {e}")

