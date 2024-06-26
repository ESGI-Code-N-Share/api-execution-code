import os
from dotenv import load_dotenv
from config import create_s3_client


load_dotenv()
s3_client = create_s3_client()


class FileService:
    def __init__(self):
        self.default_filename_code = "App."

    def createFolderCodeResources(self, codeResources):
        base_folder_code_resource = os.getenv('LOCAL_STORAGE_PATH')
        folder_path = base_folder_code_resource + "/" + codeResources.uuid

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        self.createCodeFile(codeResources.code, folder_path, codeResources.language)

        # todo : créer une condition code ressources
        self.downloadResources(codeResources.uuid)
        return folder_path

    def createCodeFile(self, code, folder_path, language):
        extension = language.getExtensionFile()
        file_path_code = folder_path + "/" + self.default_filename_code + extension
        with open(file_path_code, 'w') as file:
            file.write(code)

    def downloadResources(self, uuid):
        # todo : clean le code
        AWS_S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')
        dossier_local = os.getenv('LOCAL_STORAGE_PATH') + uuid + '/'

        if not os.path.exists(dossier_local):
            os.makedirs(dossier_local)

        continuation_token = None

        while True:
            # Préparation des paramètres de la requête
            list_params = {
                'Bucket': AWS_S3_BUCKET_NAME,
                'Prefix': uuid
            }
            if continuation_token:
                list_params['ContinuationToken'] = continuation_token

            # Lister les objets avec les paramètres spécifiés
            response = s3_client.list_objects_v2(**list_params)

            print(response)
            # Vérifier si des objets ont été trouvés
            if 'Contents' in response:
                for obj in response['Contents']:
                    # Créer le chemin local correspondant
                    chemin_local = os.path.join(dossier_local, os.path.relpath(obj['Key'], start=uuid))

                    # Créer les dossiers locaux si nécessaire
                    if not os.path.exists(os.path.dirname(chemin_local)):
                        os.makedirs(os.path.dirname(chemin_local))

                    # Télécharger le fichier
                    print(f"Téléchargement de {obj['Key']} vers {chemin_local}...")
                    s3_client.download_file(AWS_S3_BUCKET_NAME, obj['Key'], chemin_local)
                    print("Téléchargement terminé.")

            # Vérifier s'il y a plus d'objets à récupérer
            if response.get('IsTruncated'):  # Si la liste est tronquée
                continuation_token = response.get('NextContinuationToken')
            else:
                break
