import pytest
import os
import builtins
from app import app as plagiarism_app

@pytest.fixture
def client(tmp_path, monkeypatch):
    media = tmp_path / "media"
    media.mkdir()
    for name, code in [("A.py", "a=1"), ("B.py", "a=2")]:
        (media / name).write_text(code)
    monkeypatch.setenv("MEDIA_FOLDER_OVERRIDE", str(media))
    plagiarism_app.config["TESTING"] = True
    with plagiarism_app.test_client() as c:
        yield c

def test_default_method_is_difflib(client):
    resp = client.get("/check-plagiarism?file1=A.py&file2=B.py")
    assert resp.status_code == 200
    explicit = float(client.get("/check-plagiarism?file1=A.py&file2=B.py&method=difflib").get_data())
    assert float(resp.get_data()) == pytest.approx(explicit, rel=1e-6)

def test_file_not_found_returns_404(client):
    resp = client.get("/check-plagiarism?file1=NO.py&file2=A.py")
    assert resp.status_code == 404
    assert "One or both files not found" in resp.get_json()["error"]

def test_read_error_returns_500(client, monkeypatch):
    def fake_open(*args, **kwargs):
        raise IOError("disk read error")
    monkeypatch.setattr(builtins, "open", fake_open)
    resp = client.get("/check-plagiarism?file1=A.py&file2=B.py&method=difflib")
    assert resp.status_code == 500
    assert "Failed to read files" in resp.get_json()["error"]
