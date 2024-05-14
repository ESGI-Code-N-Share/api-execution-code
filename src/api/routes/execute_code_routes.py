from flask import request, jsonify
from src.api.services.execute_code_service import execute_code_service


def configure_routes(app):
    @app.route('/execute-code', methods=['POST'])
    def execute_code():
        data = request.get_json()
        response = execute_code_service(data)
        return jsonify(response)