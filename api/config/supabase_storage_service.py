import os
import uuid
from supabase import create_client, Client

class SupabaseStorageService:

    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        self.client: Client = create_client(url, key)
        self.bucket = os.getenv("SUPABASE_BUCKET", "anexos")

    def upload_file(self, file, entidade_tipo, entidade_id, franquia_id=None):
        contents = file.file.read()
        ext = file.filename.split(".")[-1]
        
        if franquia_id:
            file_path = f"{franquia_id}/{entidade_tipo}/{entidade_id}/{uuid.uuid4()}.{ext}"
        else:
            file_path = f"{entidade_tipo}/{entidade_id}/{uuid.uuid4()}.{ext}"

        self.client.storage.from_(self.bucket).upload(
            path=file_path,
            file=contents,
            file_options={"content-type": file.content_type}
        )

        public_url = self.client.storage.from_(self.bucket).get_public_url(file_path)

        return {
            "id": file_path,
            "name": file.filename,
            "webViewLink": public_url
        }

    def delete_file(self, file_path):
        self.client.storage.from_(self.bucket).remove([file_path])

    def download_file(self, file_path):
        response = self.client.storage.from_(self.bucket).download(file_path)
        return response  # retorna bytes do arquivo