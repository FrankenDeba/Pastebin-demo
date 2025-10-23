from fastapi import FastAPI
from pydantic import BaseModel

from ..models.crud import read_pastes

app = FastAPI()

class Paste(BaseModel):
    url: str

def reader(url: str | None = None):
    print("reader url:", url, type(url))
    if not url:
        return read_pastes()
    return read_pastes(url=url)
