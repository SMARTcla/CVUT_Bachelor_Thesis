def run_tests(student_module):
    """
    Executes the tests for the len_arr(arr) function.
    Returns a tuple (bool, str) indicating success and a message.
    """
    try:
        if not hasattr(student_module, 'len_arr'):
            return (0, 10, "Function 'len_arr' not found.")
        test_cases = [
            {'arr': [1, 2, 3], 'expected': 3},
            {'arr': [], 'expected': 0},
            {'arr': ['a', 'b', 'c', 'd'], 'expected': 4},
            {'arr': [True, False, True], 'expected': 3},
            {'arr': [None, None], 'expected': 2},
            {'arr': [1], 'expected': 1},
            {'arr': [1, 2, 3, 4, 5], 'expected': 5},
            {'arr': ['hello'], 'expected': 1},
            {'arr': ['a', 'b'], 'expected': 2},
            {'arr': [0, 0, 0], 'expected': 3},
        ]
        passed_tests = 0
        failed_tests = []
        for i, test in enumerate(test_cases, start=1):
            a = test['arr']
            expected = test['expected']
            try:
                result = student_module.len_arr(a)
                if result == expected:
                    passed_tests += 1
                else:
                    failed_tests.append(f"Test {i}: len_arr({a}) returned {result}, expected {expected}.")
            except Exception as e:
                failed_tests.append(f"Test {i}: Raised an exception: {e}.")
        total_tests = len(test_cases)
        if passed_tests == total_tests:
            return (passed_tests, total_tests, "All tests passed successfully.")
        else:
            return (passed_tests, total_tests, " ".join(failed_tests))

    except Exception as e:
        return (0, 10, f"Error during execution: {e}")

