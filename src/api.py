# api.py
from flask import Flask, request, jsonify
from docker_service import build_image, run_container, remove_image

app = Flask(__name__)


@app.route('/build', methods=['POST'])
def handle_build():
    data = request.get_json()
    language = data.get('language')
    # code = data.get('code')
    uuid = data.get('uuid')

    print("Language:", language)
    print("Request ID:", uuid)

    supported_languages = ['java', 'python']

    if language not in supported_languages:
        return jsonify({'error': 'Language not supported'}), 400

    docker_files_path = '../dockerfiles'
    dockerfile = f"{language}.exe.dockerfile"
    full_dockerfile_path = f"{docker_files_path}/{language}"
    tag = f"{language}-{uuid}"

    print("Dockerfile path:", full_dockerfile_path)
    print("Dockerfile:", dockerfile)
    print("Tag:", tag)

    image = build_image(full_dockerfile_path, dockerfile, tag)

    print("Image:", image)

    if image:
        container_success = run_container(tag, remove=True)
        if container_success:
            return jsonify({'success': "Container ran successfully"}), 200
        else:
            remove_image(tag)
            return jsonify({'error': "Container failed"}), 500
    else:
        return jsonify({'error': "Image not found"}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)
