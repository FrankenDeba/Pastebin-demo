from pydantic import BaseModel

class PasteText(BaseModel):
    paste: str
    url: str | None = None

