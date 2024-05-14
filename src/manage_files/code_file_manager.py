from src.api.services.docker_service import remove_image
import os


def create_code_file(language, code, uuid):
    base_dir = '../../dockerfiles'
    file_extension = 'java' if language == 'java' else 'py'
    file_name = f"App-{uuid}.{file_extension}"
    file_path = f"{base_dir}/{language}/{file_name}"

    with open(file_path, 'w') as file:
        file.write(code)

    return f"{base_dir}/{language}", f"{language}-{uuid}"


def cleanup_resources(file_path, tag):
    # if os.path.exists(file_path):
    #     os.remove(file_path)
    remove_image(tag)
