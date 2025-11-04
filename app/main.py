from fastapi import FastAPI, Request, Response
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware
import time
import logging

from app.services.logger import configure_loki_logging

try:
    configure_loki_logging()
except Exception:
    import traceback; traceback.print_exc()
    raise

logger = logging.getLogger("app")

# from services.writter import writter
# from services.reader import reader
from app.services.reader import reader
from app.services.writter import writter

from app.services.analytics import start_analytics
from app.services.logger import init_logger

from app.services.logging_middleware import RequestResponseLoggerMiddleware

from app.models.main import Pastes
from data_models import PasteText

origins = [
        "http://localhost:*",
        "http://localhost:8080",
        "http://localhost:3000",
        "http://localhost:9090",
        "http://localhost:3030",
        "http://127.0.0.1:*",
        "http://localhost:5173/*",
        "http://127.0.0.1:5173"
        # Add other allowed origins as needed
    ]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  # Allow cookies to be sent with cross-origin requests
    allow_methods=["*"],     # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],     # Allow all headers in cross-origin requests
)

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

start_analytics(app=app)

app.add_middleware(RequestResponseLoggerMiddleware) 

# init_logger(app=app)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = None
    try:
        response = await call_next(request)
        return response
    finally:
        dur_ms = int((time.perf_counter() - start) * 1000)
        # Use route name or method+path_template to avoid high-cardinality labels
        route = getattr(request.scope.get("route"), "name", request.url.path)
        logger.info(
            "HTTP request",
            extra={
                "tags": {
                    "service": "api",
                    "method": request.method,
                    "route": route,          # prefer template like /items/{id}
                    "status": str(response.status_code if response else 500),
                }
            }
        )
        logger.debug("Handled in %dms", dur_ms)

@app.get("/health", name="/health")
def health():
    logger.info("Health check OK", extra={"tags": {"service": "api"}})
    return {"ok": True}

class PasteIn(BaseModel):
    pasteText: str

@app.post("/write")
def paste(payload: PasteIn):
    logger.info("received item", extra={"tags": {"service": "api"}})
    return writter(paste=payload.pasteText)

@app.get("/read_all")
def read_pastes():
    logger.info("received item", extra={"tags": {"service": "api"}})
    return {
        "pastes": reader()
    }

@app.get("/read")
def read_paste_one(url: str):
    logger.info("received item", extra={"tags": {"service": "api"}})
    return PasteText(paste=reader(url=url).paste).paste
