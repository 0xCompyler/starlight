from celery import Celery

from app.db.db_parser import DbParser


celery = Celery(
    "tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0"
)


@celery.task(name="schema", bind=True)
def db_schema(self, db_type: str, connection_settings: dict):
    if db_type == "postgres":
        host_name = connection_settings["host_name"]
        port = connection_settings["port"]
        user_name = connection_settings["user_name"]
        password = connection_settings["password"]
        db_name = connection_settings["db_name"]
        table = connection_settings["table"]

        parser = DbParser("postgres")

        self.update_state(state="Parsing", meta={"status": "parsing"})
        parser.postgresql(host_name, port, user_name, password, db_name, table)
        self.update_state(state="Done", meta={"status": "completed"})

        return parser.columns

    if db_type == "mongo":
        pass


def task_status(task_id: str):
    result = celery.AsyncResult(task_id)
    print(task_id)
    result_dict = {
        "task_id": task_id,
        "task_status": result.status,
        "task_result": result.result,
    }

    return result_dict
