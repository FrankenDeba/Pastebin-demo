from fastapi import FastAPI
from pydantic import BaseModel

from ..models.crud import create_paste
from data_models import PasteText

app = FastAPI()

class Paste(BaseModel):
    id: int | None = None
    paste: str
    url: str

def generate_random_str() -> str:
    import random
    import string

    url = ""

    for char in range(10):
        random_char = random.choice(string.ascii_letters)
        url += random_char
    return url

@app.post("/write")
def writter(paste: str) -> PasteText:
    url = "https://mypastebin.com/" + generate_random_str()
    return create_paste(url=url, paste=paste)