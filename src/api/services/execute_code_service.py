from src.api.services.docker_service import build_image, run_container
from src.manage_files.code_file_manager import create_code_file, cleanup_resources


def execute_code_service(data):
    language = data.get('language')
    code = data.get('code')
    uuid = data.get('uuid')

    if not language or not code or not uuid:
        return {'error': 'Missing required parameters'}, 400

    if language not in ['java', 'python']:
        return {'error': 'Language not supported'}, 400

    file_path, tag = create_code_file(language, code, uuid)
    try:
        image = build_image(file_path, language, tag)
        if image:
            result, status_code = run_container(tag)
            if 'error' in result:
                return result, 400
            return {'message': 'Execution successful', 'output': result['logs']}, 200
        else:
            return {'error': "Image not found"}, 404
    finally:
        cleanup_resources(file_path, tag)
