import docker
from docker.errors import BuildError, ContainerError

client = docker.from_env()


def build_image(file_path, language, tag):
    if not file_path or not language or not tag:
        return {'error': 'Missing required parameters'}, 400
    try:
        dockerfile = f"{language}.exe.dockerfile"
        image, logs = client.images.build(
            path=file_path,
            dockerfile=dockerfile,
            tag=tag,
            rm=True,
            nocache=True)
        return image
    except BuildError as e:
        return {'error': f"Build failed due to {e}"}, 400


def run_container(tag):
    if not tag:
        return {'error': 'Missing required parameters'}, 400
    try:
        container = client.containers.run(tag, remove=True, stdout=True, stderr=True)
        return {'logs': container.decode('utf-8')}, 200
    except ContainerError as e:
        return {'error': f"Container failed due to {e}"}, 400


def remove_image(tag):
    if not tag:
        return {'error': 'Missing required parameters'}, 400
    try:
        client.images.remove(image=tag, force=True)
    except docker.errors.ImageNotFound:
        return {'error': "Image not found"}, 400
    except docker.errors.APIError as e:
        return {'error': f"Failed to remove image due to {e}"}, 400
