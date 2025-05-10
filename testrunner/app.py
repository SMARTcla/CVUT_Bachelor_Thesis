# app.py
from flask import Flask, request, jsonify
import os
import json
import importlib
import importlib.util

app = Flask(__name__)

def load_student_module(file_path):
    """Load student's code as a module from the given file path."""
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()
    module_spec = importlib.util.spec_from_loader("student_code", loader=None)
    student_module = importlib.util.module_from_spec(module_spec)
    exec(code, student_module.__dict__)
    return student_module

def get_test_module_name(file_path):
    """
    Determine the test module name based on the file path.
    Expected file path format: <username>/<Subject>/<AssignmentNumber>/<filename.py>
    For example, if file_path is "kononmi2/DSA/1/calculate_7622.py",
    the test module name will be "DSA1_tests".
    """
    parts = file_path.split(os.sep)
    if len(parts) < 6:
        raise ValueError("File path does not contain enough parts to determine test module.")
    subject = parts[4]
    assignment_number = parts[5]
    return f"{subject}{assignment_number}_tests"

@app.route('/run-tests', methods=['GET'])
def run_tests_endpoint():
    """
    Endpoint for running tests.
    When receiving a GET request with the file_path parameter, the function:
    - checks for the existence of the file,
    - determines the name of the test module and attempts to import it,
    - loads the student code,
    - runs the tests by calling the run_tests function from the test module,
    - returns the result (number of tests passed, total number of tests, message) in JSON format.
    """
    file_path = request.args.get('file_path')
    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 400
    
    try:
        test_module_name = get_test_module_name(file_path)
        test_module = importlib.import_module(f"tests.{test_module_name}")
    except Exception as e:
        return jsonify({"error": f"Failed to load test module: {str(e)}"}), 500

    try:
        student_module = load_student_module(file_path)
    except Exception as e:
        return jsonify({"error": f"Failed to load student's code: {str(e)}"}), 500

    try:
        passed_tests, total_tests, message = test_module.run_tests(student_module)
    except Exception as e:
        return jsonify({"error": f"Error during test execution: {str(e)}"}), 500

    result = {
        "passed_tests": passed_tests,
        "total_tests": total_tests,
        "message": message
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8003)
