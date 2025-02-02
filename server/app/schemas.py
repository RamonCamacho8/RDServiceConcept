from pydantic import BaseModel
from typing import List, Optional

class JobCreate(BaseModel):
    images: List[str]  # Base64 encoded images for real implementation

class JobStatus(BaseModel):
    status: str
    details: Optional[dict]
    pdf_url: Optional[str]

class AnalysisResult(BaseModel):
    image_id: str
    quality: str
    rd_present: bool
    grade: Optional[str]