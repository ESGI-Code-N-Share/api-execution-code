import os

from config import create_s3_client

s3_client = create_s3_client()


class StorageService:
    def __init__(self):
        self.s3_client = s3_client
        self.bucket_name = os.environ['AWS_S3_BUCKET_NAME']

    def get_files_from_folder(self, folder):
        files = []

        continuation_token = None

        while True:
            # Préparation des paramètres de la requête
            list_params = {
                'Bucket': self.bucket_name,
                'Prefix': folder
            }
            if continuation_token:
                list_params['ContinuationToken'] = continuation_token

            # Lister les objets avec les paramètres spécifiés
            response = s3_client.list_objects_v2(**list_params)

            # Vérifier si des objets ont été trouvés
            if 'Contents' in response:
                for obj in response['Contents']:
                    if obj['Key'] != folder:
                        files.append(obj['Key'])

            if response.get('IsTruncated'):
                continuation_token = response.get('NextContinuationToken')
            else:
                break

        return files

    def download_file(self, base, file, folder: str):
        # todo: try except
        path = os.path.join(base, os.path.relpath(file, start=folder))
        s3_client.download_file(self.bucket_name, file, path)
