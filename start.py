import os
import sys

import docker
import urllib3
from dotenv import load_dotenv
from src.api.routes import configure_routes
from src.api.services.RedisService import RedisService
from tasks import flask_app
from src.api.services.ExecutionService import ExecutionService

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()


def run():
    try:
        client = docker.from_env()
        if not client.ping():
            print("Docker client is not available")
            sys.exit(1)

        redisService = RedisService(os.getenv('REDIS_HOST'), os.getenv('REDIS_PORT'))
        executionService = ExecutionService(client)
        configure_routes(executionService, redisService)
        flask_app.run(debug=True, host=os.getenv('FLASK_HOST'), port=os.getenv('FLASK_PORT'))

        print("Client Up")

    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    run()
