from fastapi import FastAPI, Request, Response
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

# from services.writter import writter
# from services.reader import reader
from app.services.reader import reader
from app.services.writter import writter

from app.services.analytics import start_analytics
from app.services.logger import init_logger

from app.models.main import Pastes
from data_models import PasteText

origins = [
        "http://localhost:*",
        "http://localhost:8080",
        "http://localhost:3000",
        "http://localhost:9090",
        "http://localhost:3030",
        "http://127.0.0.1:*",
        "https://localhost:5173/*",
        "http://127.0.0.1:5173"
        # Add other allowed origins as needed
    ]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Allow cookies to be sent with cross-origin requests
    allow_methods=["*"],     # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],     # Allow all headers in cross-origin requests
)

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

start_analytics(app=app)

init_logger(app=app)

@app.post("/write")
def paste(pasteText: str) -> PasteText:
    # logger.info("Root endpoint accessed.")
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
