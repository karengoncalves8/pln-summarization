

from fastapi import UploadFile


class TextExtractionService:
    async def execute(self, file: UploadFile) -> str:
        data = await file.read()
        text = data.decode("utf-8")
        return text