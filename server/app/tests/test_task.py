import pytest
from app.tasks import process_images_task
from app.core.models import MockAIModels

@pytest.fixture
def mock_images():
    return [b"fake_image_data"] * 3

def test_full_pipeline_success(mock_images):
    result = process_images_task.delay(mock_images)
    assert result.get()['status'] == 'completed'
    
def test_quality_check_failure():
    class BadQualityModel(MockAIModels):
        def check_quality(self, images):
            return [{"quality": "bad"} for _ in images]
    
    pipeline = BadQualityModel()
    results = pipeline.run([b"data"])
    assert results.get('final_results') is None