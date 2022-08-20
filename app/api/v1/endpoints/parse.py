from fastapi import APIRouter

from app.schema import parser
from app.core.celery_worker import db_schema, task_status

router = APIRouter()

@router.post("/schema")
def _parse_schema(request_body: parser.SchemaParser):
    task = db_schema.delay(request_body.connection_type, request_body.connection_settings)

    return {"task_id": task.task_id}



