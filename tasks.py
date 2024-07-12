import os
import time

from dotenv import load_dotenv

import docker
import socketio
from billiard.exceptions import SoftTimeLimitExceeded
from celery import current_task
from celery.signals import task_failure, task_postrun
from config import create_app
from config import create_s3_client

load_dotenv()
SOCKETIO_SERVER_URL = os.getenv('SERVER_SOCKET_URL')

flask_app = create_app()
celery_app = flask_app.extensions["celery"]
s3_client = create_s3_client()


@celery_app.task(ignore_result=False, soft_time_limit=5, time_limit=10)
def run_container(image, folder_path):
    task_id = current_task.request.id

    client = docker.from_env()
    default_volume_app = "/home/executor/app/"
    absolute_folder_path = os.path.abspath(folder_path).lower()

    current_timestamp = time.time()

    output = client.containers.run(image, remove=True, stdout=True, stderr=True,
                                   volumes=[f'{absolute_folder_path}/:{default_volume_app}'])

    write_result(task_id, current_timestamp)

    publish_message(task_id, output.decode('utf-8'), True)
    return output.decode('utf-8')


@task_failure.connect(sender=run_container)
def task_failure_handler(sender=run_container, **kwargs):
    task_id = kwargs['task_id']
    exception = kwargs['exception']
    # todo reformat error

    if isinstance(exception, SoftTimeLimitExceeded):
        publish_message(task_id, "Timeout error", False)

    else:
        publish_message(task_id, str(exception), False)


@task_postrun.connect(sender=run_container)
def task_postrun_handler(sender=run_container, **kwargs):
    base_folder_local_storage = os.getenv('LOCAL_STORAGE_PATH')
    folder = base_folder_local_storage + sender.request.id + '/'
    files = os.listdir(folder)
    for file in files:
        os.remove(folder + file)
    os.rmdir(folder)
    print("clean files....")


def publish_message(task_id, result, status):
    clientSIO = socketio.Client()

    @clientSIO.event
    def connect():
        print('Connected to Socket.IO server')

    @clientSIO.event
    def disconnect():
        print('Disconnected from Socket.IO server')

    clientSIO.connect(SOCKETIO_SERVER_URL)

    if status:
        data_to_send = 'success:' + str(result)
    else:
        data_to_send = 'error:' + str(result)

    clientSIO.emit("task_done", {"id": task_id, "content": data_to_send})


def write_result(path_result, timestamp_to_filter):
    AWS_S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')
    destination_folder_result = path_result + '/output/'
    local_folder_result_path = os.getenv('LOCAL_STORAGE_PATH') + path_result + '/'

    for file in os.listdir(local_folder_result_path):
        current_file = local_folder_result_path + file
        created_time = os.path.getmtime(current_file)
        if created_time > timestamp_to_filter:
            s3_client.upload_file(current_file, AWS_S3_BUCKET_NAME, destination_folder_result + '{}'.format(file))

    print("Upload results on storage....")
