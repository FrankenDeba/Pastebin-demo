from fastapi import FastAPI
from pydantic import BaseModel

# from services.writter import writter
# from services.reader import reader
from app.services.reader import reader
from app.services.writter import writter

from app.models.main import Pastes
from data_models import PasteText
from fastapi.responses import JSONResponse
from fastapi import Response

app = FastAPI()

@app.post("/write")
def paste(pasteText: str) -> PasteText:
    return writter(paste=pasteText)
# Paste(url=writter(pasteText))

@app.get("/read_all")
def read_pastes():
    content = {"pastes": reader()}
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
    }
    return JSONResponse(content=content, headers=headers)

@app.options("/read_all")
def read_pastes_options():
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
    }
    return Response(status_code=204, headers=headers)

@app.get("/read")
def read_paste_one(url: str):
    print("main read_paste url:", url, type(url))
    return PasteText(paste=reader(url=url).paste).paste