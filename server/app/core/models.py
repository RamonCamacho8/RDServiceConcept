import time

class MockAIModels:
    def check_quality(self, images):
        results = []
        for _ in images:
            time.sleep(2)  # Simula 2 segundos de procesamiento por imagen
            results.append({"quality": "good"})
        return results
    
    def classify_rd(self, images):
        results = []
        for _ in images:
            time.sleep(2)  # Simula 2 segundos de procesamiento por imagen
            results.append({"rd_present": True})
        return results

    def grade_rd(self, images):
        results = []
        for _ in images:
            time.sleep(2)  # Simula 2 segundos de procesamiento por imagen
            results.append({"grade": "moderate"})
        return results
    
    def run(self, images):
        quality_results = self.check_quality(images)
        # Si se detecta alguna imagen con calidad "bad", se retorna None en final_results
        if any(result["quality"] == "bad" for result in quality_results):
            return {"final_results": None}
        
        rd_results = self.classify_rd(images)
        grade_results = self.grade_rd(images)
    
        final_results = []
        for i in range(len(images)):
            final_results.append({
                "quality": quality_results[i].get("quality", "N/A"),
                "rd_present": rd_results[i].get("rd_present", "N/A"),
                "grade": grade_results[i].get("grade", "N/A")
            })
        return {"final_results": final_results}
