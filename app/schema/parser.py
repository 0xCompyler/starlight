from pydantic import BaseModel

class SchemaParser(BaseModel):
    connection_type: str
    connection_settings: dict

class TaskStatus(BaseModel):
    task_id: str
