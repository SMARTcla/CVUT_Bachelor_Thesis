from app import (
    plagiarism_score_difflib,
    plagiarism_score_tokenize,
    plagiarism_score_ast,
    plagiarism_score_ngrams,
    plagiarism_score_winnowing
)
import pytest

code_a = """def foo():
    return 42
"""
code_b = """def foo():
    return 42
"""
code_c = """def bar():
    return 0
"""
code_d = """print('Hello, world!')
"""

@pytest.mark.parametrize("func, expected_full", [
    (plagiarism_score_difflib, 100.0),
    (plagiarism_score_tokenize, 100.0),
    (plagiarism_score_ast, 100.0),
    (plagiarism_score_ngrams, 100.0),
    (plagiarism_score_winnowing, 100.0),
])
def test_full_similarity(func, expected_full):
    assert pytest.approx(func(code_a, code_b), rel=1e-6) == expected_full

@pytest.mark.parametrize("func", [
    plagiarism_score_difflib,
    plagiarism_score_tokenize,
    plagiarism_score_ast,
    plagiarism_score_ngrams,
    plagiarism_score_winnowing,
])
def test_low_similarity_for_unrelated(func):
    score = func(code_a, code_d)
    assert score < 50.0, f"Expected low similarity, got {score}"

@pytest.mark.parametrize("func", [
    plagiarism_score_difflib,
    plagiarism_score_tokenize,
    plagiarism_score_ast,
    plagiarism_score_ngrams,
    plagiarism_score_winnowing,
])
def test_partial_similarity(func):
    score = func(code_a, code_c)
    assert 0.0 < score < 100.0, f"Expected partial similarity, got {score}"