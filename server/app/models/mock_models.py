import random
import time
from typing import Dict

def quality_model(image: bytes) -> float:
    """Mock model for quality check"""
    time.sleep(0.5)  # Simulate processing time
    return random.uniform(0.7, 1.0)  # Always passes for demo

def classification_model(image: bytes) -> float:
    """Mock binary classification model"""
    time.sleep(1.0)
    return random.uniform(0.3, 0.8)  # Random results

def grading_model(image: bytes) -> Dict:
    """Mock multi-class grading model"""
    time.sleep(1.5)
    return {
        'grade': random.randint(1, 3),
        'confidence': round(random.uniform(0.5, 0.95), 2)
    }