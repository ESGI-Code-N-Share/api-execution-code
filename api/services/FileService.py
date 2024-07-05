import os
from dotenv import load_dotenv

from api.services.StorageService import StorageService

load_dotenv()


class FileService:
    def __init__(self):
        self.default_filename_code = "App."
        self.storageService = StorageService()
        self.base_folder_local_storage = os.getenv('LOCAL_STORAGE_PATH')

    def createFolderCodeResources(self, codeResources):
        folder_path = self.base_folder_local_storage + "/" + codeResources.uuid

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        self.createCodeFile(codeResources.code, folder_path, codeResources.language)

        # todo : adapt when Corentin's pipeline
        self.downloadResources(codeResources.uuid)
        return folder_path

    def createCodeFile(self, code, folder_path, language):
        extension = language.getExtensionFile()
        file_path_code = folder_path + "/" + self.default_filename_code + extension
        with open(file_path_code, 'w') as file:
            file.write(code)
            file.close()

    def downloadResources(self, uuid):
        local_folder = self.base_folder_local_storage + uuid

        if not os.path.exists(local_folder):
            os.makedirs(local_folder)

        files = self.storageService.get_files_from_folder(uuid + '/input/')

        for file in files:
            print(file)
            self.storageService.download_file(local_folder, file, uuid + '/input/')

        print("Download inputs files => Done....")