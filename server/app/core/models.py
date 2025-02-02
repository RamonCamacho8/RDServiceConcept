class MockAIModels:
    def check_quality(self, images):
        return [{"quality": "good"} for _ in images]
    
    def classify_rd(self, images):
        return [{"rd_present": True} for _ in images]
    
    def grade_rd(self, images):
        return [{"grade": "moderate"} for _ in images]
    
    def run(self, images):
        # Pipeline logic
        return {"final_results": [...]}