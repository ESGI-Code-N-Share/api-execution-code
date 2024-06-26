import os
import time


from dotenv import load_dotenv

import docker
import socketio
from billiard.exceptions import SoftTimeLimitExceeded
from celery import current_task
from celery.signals import task_failure, task_success
from config import create_app
from config import create_s3_client

load_dotenv()
SOCKETIO_SERVER_URL = os.getenv('SERVER_SOCKET_URL')

flask_app = create_app()
celery_app = flask_app.extensions["celery"]
s3_client = create_s3_client()


@celery_app.task(ignore_result=False, soft_time_limit=15, time_limit=20)
def run_container(image, folder_path):
    task_id = current_task.request.id

    client = docker.from_env()
    default_volume_app = "/home/executor/app/"
    absolute_folder_path = os.path.abspath(folder_path).lower()

    ts = time.time()
    print(ts)

    output = client.containers.run(image, remove=True, stdout=True, stderr=True,
                                   volumes=[f'{absolute_folder_path}/:{default_volume_app}'])

    write_result(task_id, ts)
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


@task_success.connect(sender=run_container)
def task_failure_handler(sender=run_container, **kwargs):
    task_id = kwargs['task_id']
    print("je dois tout clean")
    # clean le folder result

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


def write_result(path_result, ts):
    base_folder_code_resource = os.getenv('LOCAL_STORAGE_PATH')
    AWS_S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')

    folder_result = path_result + '/output/'
    complete_folder_path = base_folder_code_resource + path_result + '/'
    print(complete_folder_path)

    s3_client.put_object(Bucket=AWS_S3_BUCKET_NAME, Key=folder_result)

    for file in os.listdir(complete_folder_path):
        created_time = os.path.getmtime(complete_folder_path + file)
        if created_time > ts:
            s3_client.upload_file(complete_folder_path + file, AWS_S3_BUCKET_NAME, folder_result + '{}'.format(file))

    print("Upload results")
