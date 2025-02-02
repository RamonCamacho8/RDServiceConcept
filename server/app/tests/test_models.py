from app.core.models import MockAIModels
import pytest

def test_quality_check():
    model = MockAIModels()
    images = [b"data"] * 3
    results = model.check_quality(images)
    assert len(results) == 3
    assert all(r["quality"] == "good" for r in results)

def test_rd_classification():
    model = MockAIModels()
    images = [b"data"] * 2
    results = model.classify_rd(images)
    assert len(results) == 2
    assert all(r["rd_present"] is True for r in results)

def test_rd_grading():
    model = MockAIModels()
    images = [b"data"] * 4
    results = model.grade_rd(images)
    assert len(results) == 4
    assert all(r["grade"] == "moderate" for r in results)