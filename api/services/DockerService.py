from docker.errors import ImageNotFound, APIError

from api.exceptions.ImagePulledNotFound import ImagePulledNotFound
from api.services.FileService import FileService


class DockerService:
    def __init__(self, client):
        self.fileService = FileService()
        self.client = client
        self.registry = "codenshareregistry/edc"
        self.default_volume_app = "/home/executor/app/"

    def get_image(self, language):
        version = "latest" if not language.version else language.version
        image_name = f"{self.registry}-{language.name}:{version}"

        try:
            image = self.client.images.get(image_name)
        except ImageNotFound:
            image = self.pull_image(image_name)

        return image

    def pull_image(self, image_name):
        try:
            return self.client.images.pull(image_name)
        except APIError:
            raise ImagePulledNotFound()