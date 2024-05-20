import sys

import docker
import urllib3
from dotenv import load_dotenv
from flask import Flask
from flask import request, jsonify

from api.models.CodeResources import CodeResources
from api.models.LanguageModel import Language
from api.services.ExecutionService import ExecutionService

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()


def run():
    try:
        client = docker.from_env()
        if not client.ping():
            print("Docker client is not available")
            sys.exit(1)

        executionService = ExecutionService(client)
        app = Flask(__name__)
        configure_routes(app, executionService)
        app.run(debug=True, port=5000)

        print("Client Up")
    except:
        print("Docker host not available")
        sys.exit(1)


def configure_routes(app, executionService):
    @app.route('/execute-code', methods=['POST'])
    def execute_code():
        try:
            data = request.get_json()

            language_name = data.get('language')
            version = data.get('version')
            code = data.get('code')
            uuid = data.get('uuid')

            if not language_name or not code or not uuid or not version:
                return {'error': 'Missing required parameters'}, 400

            language = Language(language_name, version)
            codeResource = CodeResources(uuid, code, language)
            output = executionService.execute_code(codeResource)
            return jsonify({'result': output})

        except Exception as a:
            print(a)
            return jsonify({'error': str(a)}), 400

    @app.route('/up', methods=['GET'])
    def healthcheck():
        return 'up'


if __name__ == "__main__":
    run()
