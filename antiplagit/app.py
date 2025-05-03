#!/usr/bin/env python
from flask import Flask, request, jsonify
import os
import json
import difflib
import tokenize
import io
import ast

app = Flask(__name__)

def plagiarism_score_difflib(code1, code2):
    ratio = difflib.SequenceMatcher(None, code1, code2).ratio()
    return ratio * 100

def plagiarism_score_tokenize(code1, code2):
    def tokenize_code(code):
        tokens = []
        try:
            g = tokenize.generate_tokens(io.StringIO(code).readline)
            for toknum, tokval, _, _, _ in g:
                if toknum not in (tokenize.INDENT, tokenize.DEDENT, tokenize.NEWLINE, tokenize.NL, tokenize.COMMENT):
                    tokens.append(tokval)
        except Exception:
            pass
        return " ".join(tokens)
    tokens1 = tokenize_code(code1)
    tokens2 = tokenize_code(code2)
    ratio = difflib.SequenceMatcher(None, tokens1, tokens2).ratio()
    return ratio * 100

def plagiarism_score_ast(code1, code2):
    try:
        tree1 = ast.parse(code1)
        tree2 = ast.parse(code2)
        dump1 = ast.dump(tree1)
        dump2 = ast.dump(tree2)
        ratio = difflib.SequenceMatcher(None, dump1, dump2).ratio()
        return ratio * 100
    except Exception:
        return 0

def plagiarism_score_ngrams(code1, code2, n=5):
    def ngrams(text, n):
        return {text[i:i+n] for i in range(len(text)-n+1)}
    ngrams1 = ngrams(code1, n)
    ngrams2 = ngrams(code2, n)
    if not ngrams1 or not ngrams2:
        return 0
    intersection = ngrams1.intersection(ngrams2)
    union = ngrams1.union(ngrams2)
    similarity = len(intersection) / len(union)
    return similarity * 100

def plagiarism_score_winnowing(code1, code2, k=5, t=4):
    def hash_ngrams(code, k):
        return [hash(code[i:i+k]) for i in range(len(code)-k+1)]
    
    def winnow(hashes, t):
        fingerprints = set()
        if len(hashes) < t:
            return set(hashes)
        for i in range(len(hashes)-t+1):
            window = hashes[i:i+t]
            fingerprints.add(min(window))
        return fingerprints

    hashes1 = hash_ngrams(code1, k)
    hashes2 = hash_ngrams(code2, k)
    fingerprints1 = winnow(hashes1, t)
    fingerprints2 = winnow(hashes2, t)
    if not fingerprints1 or not fingerprints2:
        return 0
    intersection = fingerprints1.intersection(fingerprints2)
    union = fingerprints1.union(fingerprints2)
    similarity = len(intersection) / len(union)
    return similarity * 100

@app.route('/check-plagiarism', methods=['GET'])
def check_plagiarism():
    """
    Endpoint для проверки плагиата между двумя файлами.
    Ожидает параметры:
      - file1: путь к первому файлу (относительный путь внутри тома /app/media)
      - file2: путь ко второму файлу
      - method: метод сравнения ("difflib", "tokenize", "ast", "ngrams", "winnowing")
    Возвращает JSON с оценкой схожести.
    """
    file1 = request.args.get('file1')
    file2 = request.args.get('file2')
    method = request.args.get('method', 'difflib')

    if not file1 or not file2:
        return jsonify({"error": "Both file1 and file2 parameters are required"}), 400

    path1 = os.path.join('/app/media', file1)
    path2 = os.path.join('/app/media', file2)

    if not os.path.exists(path1) or not os.path.exists(path2):
        return jsonify({"error": "One or both files not found"}), 404

    try:
        with open(path1, "r", encoding="utf-8") as f:
            code1 = f.read()
        with open(path2, "r", encoding="utf-8") as f:
            code2 = f.read()
    except Exception as e:
        return jsonify({"error": f"Failed to read files: {str(e)}"}), 500

    if method == 'difflib':
        score = plagiarism_score_difflib(code1, code2)
    elif method == 'tokenize':
        score = plagiarism_score_tokenize(code1, code2)
    elif method == 'ast':
        score = plagiarism_score_ast(code1, code2)
    elif method == 'ngrams':
        score = plagiarism_score_ngrams(code1, code2)
    elif method == 'winnowing':
        score = plagiarism_score_winnowing(code1, code2)
    else:
        return jsonify({"error": "Unknown method"}), 400

    result = {
        "method": method,
        "score": score
    }
    return jsonify(result["score"])

if __name__ == "__main__":
    # Сервис будет слушать порт 8004
    app.run(host="0.0.0.0", port=8004)
