import os

import docker

from config import create_app
from celery import shared_task

flask_app = create_app()
celery_app = flask_app.extensions["celery"]


@shared_task(ignore_result=False)
def run_container(image, folder_path) -> str:
    client = docker.from_env()

    default_volume_app = "/home/executor/app/"

    absolute_folder_path = os.path.abspath(folder_path).lower()
    output = client.containers.run(image, remove=True, stdout=True, stderr=True,
                                   volumes=[f'{absolute_folder_path}/:{default_volume_app}'])

    return output.decode('utf-8')
