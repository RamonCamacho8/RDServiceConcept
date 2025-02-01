import os
import shutil
import pytest
from fastapi.testclient import TestClient
from app.main import app, UPLOAD_DIR, REPORT_DIR

client = TestClient(app)

@pytest.fixture(autouse=True)
def run_around_tests():
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)
    yield
    shutil.rmtree(UPLOAD_DIR, ignore_errors=True)
    shutil.rmtree(REPORT_DIR, ignore_errors=True)

def test_upload_no_files():
    response = client.post("/upload", files=[])
    assert response.status_code == 422

def test_upload_files():
    file_content = b"fake image data"
    files = {"files": ("test.jpg", file_content, "image/jpeg")}
    response = client.post("/upload", files=files)
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
