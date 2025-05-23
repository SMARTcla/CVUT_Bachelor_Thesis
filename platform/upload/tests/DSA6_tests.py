def run_tests(student_module):
    """
    Executes the tests for the pow_cal function.
    Returns a tuple (bool, str) indicating success and a message.
    """
    try:
        if not hasattr(student_module, 'pow_cal'):
            return False, "Function 'pow_cal' not found."
        test_cases = [
            {'a': 2, 'b': 3, 'expected': 8},
            {'a': -1, 'b': 2, 'expected': 1},
            {'a': 0, 'b': 0, 'expected': 1}, 
            {'a': 5, 'b': 4, 'expected': 625},
            {'a': 10, 'b': 3, 'expected': 1000},
        ]

        for i, test in enumerate(test_cases, 1):
            a = test['a']
            b = test['b']
            expected = test['expected']
            try:
                result = student_module.pow_cal(a, b)
                if result != expected:
                    return False, f"Test {i} failed: pow_cal({a}, {b}) returned {result}, expected {expected}."
            except Exception as e:
                return False, f"Test {i} raised an exception: {e}"

        return True, "All tests passed successfully."

    except Exception as e:
        return False, f"Error during execution: {e}"

