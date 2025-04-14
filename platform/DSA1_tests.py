def run_tests(student_module):
    """
    Executes the tests for the calculate(a, b) function.
    Returns a tuple (passed_tests, total_tests, message).
    """
    try:
        if not hasattr(student_module, 'calculate'):
            return (0, 10, "Function 'calculate' not found.")

        test_cases = [
            {'a': 2, 'b': 3, 'expected': 5},
            {'a': -1, 'b': 1, 'expected': 0},
            {'a': 0, 'b': 0, 'expected': 0},
            {'a': 10, 'b': 5, 'expected': 15},
            {'a': -5, 'b': -10, 'expected': -15},
            {'a': 100, 'b': 200, 'expected': 300},
            {'a': 1.5, 'b': 2.5, 'expected': 4.0},
            {'a': -2.5, 'b': 2.5, 'expected': 0.0},
            {'a': 1000, 'b': 2000, 'expected': 3000},
            {'a': 123, 'b': 456, 'expected': 579},
        ]

        passed_tests = 0
        failed_tests = []
        for i, test in enumerate(test_cases, start=1):
            a = test['a']
            b = test['b']
            expected = test['expected']
            try:
                result = student_module.calculate(a, b)
                if result == expected:
                    passed_tests += 1
                else:
                    failed_tests.append(f"Test {i}: calculate({a}, {b}) returned {result}, expected {expected}.")
            except Exception as e:
                failed_tests.append(f"Test {i}: Raised an exception: {e}.")

        total_tests = len(test_cases)
        if passed_tests == total_tests:
            return (passed_tests, total_tests, "All tests passed successfully.")
        else:
            return (passed_tests, total_tests, " ".join(failed_tests))

    except Exception as e:
        return (0, 10, f"Error during execution: {e}")

