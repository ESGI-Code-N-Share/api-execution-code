import os
from dotenv import load_dotenv

load_dotenv()


class FileService:
    def __init__(self):
        self.default_filename_code = "App."

    def createFolderCodeResources(self, codeResources):
        base_folder_code_resource = os.getenv('STORAGE_PATH')
        folder_path = base_folder_code_resource + "/" + codeResources.uuid

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        self.createCodeFile(codeResources.code, folder_path, codeResources.language)
        return folder_path

    def createCodeFile(self, code, folder_path, language):
        extension = language.getExtensionFile()
        file_path_code = folder_path + "/" + self.default_filename_code + extension
        with open(file_path_code, 'w') as file:
            file.write(code)