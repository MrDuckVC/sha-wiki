import logging

from main.celery import app


logger = logging.getLogger(__name__)


@app.task
def update_data():
    # TODO: Implement data update task.
    pass
