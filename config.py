import os

import boto3
from celery import Celery, Task
from dotenv import load_dotenv
from flask import Flask

load_dotenv()


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        CELERY=dict(
            broker_url=f"pyamqp://{os.getenv('RABBITMQ_USER')}:{os.getenv('RABBITMQ_PASSWORD')}@{os.getenv('RABBITMQ_HOST')}:{os.getenv('RABBITMQ_PORT')}//",
            result_backend=f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/0",
            task_ignore_result=True,
        ),
    )
    app.config.from_prefixed_env()
    celery_init_app(app)
    return app


def create_s3_client():
    s3_client = boto3.client(
        service_name='s3',
        region_name=f"{os.getenv('AWS_REGION')}",
        aws_access_key_id=f"{os.getenv('AWS_ACCESS_KEY')}",
        aws_secret_access_key=f"{os.getenv('AWS_SECRET_KEY')}"
    )
    return s3_client
