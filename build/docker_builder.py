# docker_builder.py
import docker
from docker.errors import BuildError, ContainerError

client = docker.from_env()


def build_image(docker_file_path, dockerfile, tag, build_args=None):
    try:
        build_args = build_args or {}
        image, logs = client.images.build(
            path=docker_file_path,
            dockerfile=dockerfile,
            tag=tag,
            buildargs=build_args,
            rm=True,
            nocache=True)
        return image
    except BuildError as e:
        print(f"Build failed due to {e}")
        return None


def run_container(image_tag, remove):
    try:
        container = client.containers.run(image_tag, remove=remove)
        print(container)
    except ContainerError as e:
        print(f"Container failed due to {e}")
        return None


if __name__ == "__main__":
    image_built = build_image('../dockerfiles/java', 'java.exe.dockerfile', 'java', {})
    if image_built:
        print("Image built successfully")
        run_container('java', remove=True)
        print("Container started")
    else:
        print("Failed to build image")
