import fitz
from supabase import Client


class StorageService:
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client

    def extract_text_from_pdf(self, file_content: bytes) -> str:
        text = ""
        with fitz.open(stream=file_content, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text

    async def upload_to_storage(
        self,
        bucket_name: str,
        file_content: bytes,
        filename: str,
        content_type: str,
    ):
        try:
            self.supabase.storage.from_(bucket_name).upload(
                path=filename,
                file=file_content,
                file_options={"content-type": content_type},
            )
        except Exception as e:
            if "already exists" not in str(e):
                raise e