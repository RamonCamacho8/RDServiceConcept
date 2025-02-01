from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid
import os
from app.tasks import process_images_task

app = FastAPI()

# Configurar CORS (se permite cualquier origen, ajustar según necesidad)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
REPORT_DIR = "reports"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

@app.post("/upload")
async def upload_images(files: list[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No se han subido imágenes")
    
    # Generar identificador único para la tarea
    task_id = str(uuid.uuid4())
    task_upload_dir = os.path.join(UPLOAD_DIR, task_id)
    os.makedirs(task_upload_dir, exist_ok=True)
    
    saved_files = []
    for file in files:
        file_path = os.path.join(task_upload_dir, file.filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        saved_files.append(file_path)
    
    # Enviar tarea a Celery (la tarea retorna el estado y el reporte cuando finaliza)
    task = process_images_task.delay(task_id, saved_files)
    return {"task_id": task.id}

@app.get("/status/{task_id}")
def get_status(task_id: str):
    from celery.result import AsyncResult
    res = AsyncResult(task_id)
    return {"task_id": task_id, "status": res.status, "result": res.result}

@app.get("/report/{task_id}")
def get_report(task_id: str):
    report_path = os.path.join(REPORT_DIR, f"{task_id}.pdf")
    if not os.path.exists(report_path):
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return FileResponse(report_path, media_type='application/pdf', filename=f"Reporte_{task_id}.pdf")
