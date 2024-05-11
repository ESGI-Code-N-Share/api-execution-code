from flask import Flask, request, jsonify
from docker_service import build_image, run_container, remove_image
import os

app = Flask(__name__)


@app.route('/build', methods=['POST'])
def handle_build():
    data = request.get_json()
    language = data.get('language')
    code = data.get('code')
    uuid = data.get('uuid')

    if language not in ['java', 'python']:
        return jsonify({'error': 'Language not supported'}), 400

    docker_files_path = '../dockerfiles'
    if language == 'java':
        file_name = f"App-{uuid}.java"
    else:
        file_name = f"App-{uuid}.py"
    full_file_path = f"{docker_files_path}/{language}/{file_name}"
    full_dockerfile_path = f"{docker_files_path}/{language}"
    dockerfile = f"{language}.exe.dockerfile"
    tag = f"{language}-{uuid}"

    try:
        with open(full_file_path, 'w') as file:
            file.write(code)

        image = build_image(full_dockerfile_path, dockerfile, tag)

        if image:
            container_success = run_container(tag, remove=True)
            if container_success:
                return jsonify({'success': "Container ran successfully"}), 200
            else:
                return jsonify({'error': "Container failed"}), 500
        else:
            return jsonify({'error': "Image not found"}), 400

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500

    finally:
        if os.path.exists(full_file_path):
            os.remove(full_file_path)
        remove_image(tag)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
