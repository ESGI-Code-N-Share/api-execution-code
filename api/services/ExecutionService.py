from tasks import run_container
from api.services.DockerService import DockerService
from api.services.FileService import FileService


class ExecutionService:
    def __init__(self, client):
        self.client = client
        self.fileService = FileService()
        self.dockerService = DockerService(client)

    def execute_code(self, codeResources):
        image = self.dockerService.get_image(codeResources.language)
        folder_path = self.fileService.createFolderCodeResources(codeResources)
        res = run_container.delay(image.tags[0], folder_path)
        return res
