import os

from dotenv import load_dotenv

import docker
import socketio
from billiard.exceptions import SoftTimeLimitExceeded
from celery import current_task
from celery.signals import task_failure

from config import create_app

flask_app = create_app()
celery_app = flask_app.extensions["celery"]

load_dotenv()

# maybe change to https
SOCKETIO_SERVER_URL = f"http://{os.getenv('SERVER_SOCKET_HOST')}:{os.getenv('SERVER_SOCKET_PORT')}"


@celery_app.task(ignore_result=False, soft_time_limit=15, time_limit=20)
def run_container(image, folder_path):
    task_id = current_task.request.id

    client = docker.from_env()
    default_volume_app = "/home/executor/app/"
    absolute_folder_path = os.path.abspath(folder_path).lower()

    output = client.containers.run(image, remove=True, stdout=True, stderr=True,
                                   volumes=[f'{absolute_folder_path}/:{default_volume_app}'])
    publish_message(task_id, output.decode('utf-8'))
    return output.decode('utf-8')


@task_failure.connect(sender=run_container)
def task_failure_handler(sender=run_container, **kwargs):
    task_id = kwargs['task_id']
    exception = kwargs['exception']
    # todo reformat error

    if isinstance(exception, SoftTimeLimitExceeded):
        publish_message(task_id, "Timeout error")

    else:
        publish_message(task_id, str(exception))


def publish_message(task_id, result):
    clientSIO = socketio.Client()

    @clientSIO.event
    def connect():
        print('Connected to Socket.IO server')

    @clientSIO.event
    def disconnect():
        print('Disconnected from Socket.IO server')

    clientSIO.connect(SOCKETIO_SERVER_URL)
    clientSIO.emit("task_done", {"id": task_id, "content": result})
