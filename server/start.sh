#!/bin/bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
celery -A app.tasks worker --loglevel=info