import os

from docker.errors import ImageNotFound, APIError

from api.exceptions.LanguageNotSupported import LanguageNotSupported
from api.services.FileService import FileService


class DockerService:
    def __init__(self, client):
        self.fileService = FileService()
        self.client = client
        self.registry = "codenshareregistry/edc"
        self.default_volume_app = "/home/java/app/"

    def get_image(self, language):
        image_name = f"{self.registry}-{language.name}:{language.version}"

        try:
            image = self.client.images.get(image_name)
        except ImageNotFound:
            image = self.pull_image(image_name)

        return image

    def pull_image(self, image_name):
        try:
            return self.client.images.pull(image_name)
        except APIError:
            raise LanguageNotSupported()

    def run_container(self, image, folder_path):
        absolute_folder_path = os.path.abspath(folder_path).lower() #todo: Abd don't to add lower before push
        output = self.client.containers.run(image, remove=True, stdout=True, stderr=True, volumes=[f'{absolute_folder_path}/:{self.default_volume_app}'])
        return output.decode('utf-8')
