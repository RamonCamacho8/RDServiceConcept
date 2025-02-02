from fastapi.testclient import TestClient
from app.main import app

from app.tasks import celery
celery.conf.task_always_eager = True
celery.conf.task_eager_propagates = True


client = TestClient(app)



def test_create_job():
    response = client.post("/jobs/", files={"files": ("test.png", b"test")})
    assert response.status_code == 200
    assert "job_id" in response.json()