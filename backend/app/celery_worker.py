from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

# Opcional: asegurarte de que se guarden los resultados
celery_app.conf.task_ignore_result = False
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)
