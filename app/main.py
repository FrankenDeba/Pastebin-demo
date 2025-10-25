from fastapi import FastAPI
from pydantic import BaseModel

# from services.writter import writter
# from services.reader import reader
from app.services.reader import reader
from app.services.writter import writter

from app.services.analytics import start_analytics

from app.models.main import Pastes
from data_models import PasteText

app = FastAPI()

start_analytics(app=app)

@app.post("/write")
def paste(pasteText: str) -> PasteText:
    return writter(paste=pasteText)
# Paste(url=writter(pasteText))

@app.get("/read_all")
def read_pastes():
    return {
        "pastes": reader()
    }

@app.get("/read")
def read_paste_one(url: str):
    print("main read_paste url:", url, type(url))
    return PasteText(paste=reader(url=url).paste).paste
