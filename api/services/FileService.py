import os


class FileService:
    def __init__(self):
        self.base_folder_code_resource = "./coderesources"
        self.default_filename_code = "App."

    def createFolderCodeResources(self, codeResources):
        folder_path = self.base_folder_code_resource + "/" + codeResources.uuid

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        self.createCodeFile(codeResources.code, folder_path, codeResources.language)

        # todo : create assets file

        return folder_path

    def createCodeFile(self, code, folder_path, language):
        extension = language.getExtensionFile()
        file_path_code = folder_path + "/" + self.default_filename_code + extension
        with open(file_path_code, 'w') as file:
            file.write(code)
