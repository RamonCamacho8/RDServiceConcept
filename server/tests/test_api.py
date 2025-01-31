from app.tasks import process_image_task
import pytest

@pytest.mark.celery(result_backend='redis://redis:6379/0')
def test_celery_task(celery_worker):
    mock_images = [b"fake_image_data"]
    result = process_image_task.delay(mock_images)
    assert result.get(timeout=10)['status'] == 'success'