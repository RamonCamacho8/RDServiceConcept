from fastapi import FastAPI, UploadFile, WebSocket
from fastapi.responses import FileResponse
from celery.result import AsyncResult
import uuid
from .tasks import process_image_task

app = FastAPI()

@app.post("/upload")
async def upload_images(files: list[UploadFile]):
    task_id = str(uuid.uuid4())
    images = [await file.read() for file in files]
    process_image_task.apply_async(args=(images,), task_id=task_id)
    return {"task_id": task_id}

@app.websocket("/ws/{task_id}")
async def websocket_progress(websocket: WebSocket, task_id: str):
    await websocket.accept()
    while True:
        result = AsyncResult(task_id, app=process_image_task.app)
        progress = result.info.get('progress', 0) if result.info else 0
        stage = result.info.get('stage', 'Pending') if result.info else 'Pending'
        
        await websocket.send_json({
            "progress": progress,
            "stage": stage,
            "status": result.status
        })
        
        if result.ready():
            break

@app.get("/download/{task_id}")
async def download_pdf(task_id: str):
    return FileResponse(
        f"reports/{task_id}.pdf",
        media_type="application/pdf",
        filename="report.pdf"
    )