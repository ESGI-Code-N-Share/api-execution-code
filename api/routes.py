from typing import Any

from celery.result import AsyncResult
from flask import request, jsonify, Response

from api.models.CodeResources import CodeResources
from api.models.LanguageModel import Language
from tasks import flask_app


def configure_routes(executionService, redisService):
    @flask_app.post("/execute-code")
    def execute_code():
        try:
            data = request.get_json()

            language_name = data.get('language')
            version = data.get('version')
            code = data.get('code')
            uuid = data.get('uuid')

            if not language_name or not code or not uuid:
                return {'error': 'Missing required parameters'}, 400

            language = Language(language_name, version)
            codeResource = CodeResources(uuid, code, language)
            task = executionService.execute_code(codeResource)
            redisService.set(task.id)
            return jsonify({'taskId': task.id})

        except Exception as a:
            print(a)
            return jsonify({'error': str(a)}), 400

    @flask_app.get("/result")
    def task_result() -> dict[str, Any] | tuple[Response, int]:
        task_id = request.args.get('taskId')

        try:
            redisService.checkIfKeyExist(task_id)
            task = AsyncResult(task_id)

            if task.successful():
                return jsonify({'status': 'Success', 'result': str(task.result)}), 200

            elif task.state == 'PENDING':
                return jsonify({'status': 'Running'}), 200

            else:
                return jsonify({'status': 'Failed', 'result': str(task.result)}), 500

        except Exception as a:
            print(a)
            return jsonify({'error': str(a)}), 404

    @flask_app.get("/up")
    def healthcheck():
        return 'up'
