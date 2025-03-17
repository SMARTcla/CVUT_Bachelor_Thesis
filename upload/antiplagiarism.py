import difflib
import tokenize
import io
import ast

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
    # Simplified Winnowing algorithm
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