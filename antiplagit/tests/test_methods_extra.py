# antiplagit/tests/test_methods_extra.py

import pytest
import tempfile
import os
from app import (
    plagiarism_score_difflib,
    plagiarism_score_tokenize,
    plagiarism_score_ast,
    plagiarism_score_ngrams,
    plagiarism_score_winnowing
)

code_simple = "a = 1"
code_with_comments = "# comment\na = 1  # end"
code_diff_format = "a=1"
code_short = "ab"
code_single = "x"

@pytest.mark.parametrize("func", [
    plagiarism_score_difflib,
    plagiarism_score_tokenize,
    plagiarism_score_ast,
    plagiarism_score_ngrams,
    plagiarism_score_winnowing,
])
def test_tokenize_ignores_comments(func):
    assert pytest.approx(plagiarism_score_tokenize(code_simple, code_with_comments), rel=1e-6) == 100.0

def test_ast_ignores_whitespace_and_formatting():
    assert pytest.approx(plagiarism_score_ast(code_simple, code_diff_format), rel=1e-6) == 100.0

def test_ngrams_short_input_zero():
    assert pytest.approx(plagiarism_score_ngrams(code_short, code_simple), rel=1e-6) == 0.0
    assert pytest.approx(plagiarism_score_ngrams(code_simple, code_single), rel=1e-6) == 0.0

def test_winnowing_short_input_zero():
    assert pytest.approx(plagiarism_score_winnowing(code_short, code_simple), rel=1e-6) == 0.0
    assert pytest.approx(plagiarism_score_winnowing(code_simple, code_single), rel=1e-6) == 0.0

def test_partial_similarity_varies_by_method():
    score_d = plagiarism_score_difflib(code_simple, "a = 2")
    score_t = plagiarism_score_tokenize(code_simple, "a = 2")
    score_a = plagiarism_score_ast(code_simple, "a = 2")
    assert score_d != score_t or score_t != score_a
