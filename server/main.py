import os
import uuid
from typing import List
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from tasks import process_images
from celery.result import AsyncResult
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


origins = [
    "http://localhost:3000",  # your client URL
    # Add other allowed origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Allows requests from these origins
    allow_credentials=True,
    allow_methods=["*"],            # Allows all HTTP methods
    allow_headers=["*"],            # Allows all headers
)


# Endpoint to upload images and start the pipeline.
@app.post("/upload")
async def upload_images(files: List[UploadFile] = File(...)):
    job_id = str(uuid.uuid4())
    job_dir = os.path.join("uploads", job_id)
    os.makedirs(job_dir, exist_ok=True)
    file_paths = []
    for file in files:
        file_path = os.path.join(job_dir, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        file_paths.append(file_path)
    task = process_images.apply_async(args=[job_id, file_paths])
    return {"job_id": task.id}

# Endpoint to check the status of the pipeline.
@app.get("/status/{job_id}")
def get_status(job_id: str):
    task = AsyncResult(job_id, app=process_images.app)
    return {"status": task.state, "info": task.info}

# Endpoint to retrieve the generated PDF.
@app.get("/pdf/{job_id}")
def get_pdf(job_id: str):
    pdf_path = os.path.join("reports", f"{job_id}.pdf")
    if os.path.exists(pdf_path):
        return FileResponse(pdf_path, media_type="application/pdf", filename=f"{job_id}.pdf")
    return {"error": "PDF not found"}
