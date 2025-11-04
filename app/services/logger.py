from fastapi import FastAPI, Request, Response
import time
import logging
import logging.config
import logging_loki

# logging_setup.py
import logging, logging.config

LOKI_URL = "http://127.0.0.1:3100/loki/api/v1/push"  # change if needed

def configure_loki_logging():
    cfg = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {"format": "%(asctime)s %(levelname)s %(name)s - %(message)s"},
        },
        "handlers": {
            # Use "()" factory style — more reliable for 3rd-party handlers
            "loki": {
                "()": "logging_loki.LokiHandler",   # if this fails, try "logging_loki.handlers.LokiHandler"
                "level": "INFO",
                "formatter": "default",
                "url": LOKI_URL,
                "tags": {"application": "pastebin-demo", "env": "dev"},
                "version": "1",
                # "timeout": 5,
                # Only set these if you actually need them:
                # "auth": ("username", "password"),
                # "insecure": True,    # for skipping TLS verify on some versions
                # (avoid "verify": False here — some versions don't accept it)
            },
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": "INFO",
            },
        },
        "root": {"level": "INFO", "handlers": ["console", "loki"]},
        "loggers": {
            "uvicorn": {"level": "INFO", "handlers": ["console", "loki"], "propagate": False},
            "uvicorn.error": {"level": "INFO", "handlers": ["console", "loki"], "propagate": False},
            "uvicorn.access": {"level": "INFO", "handlers": ["console", "loki"], "propagate": False},
            "fastapi": {"level": "INFO", "handlers": ["console", "loki"], "propagate": False},
        },
    }

    # Helpful while debugging handler config:
    logging.raiseExceptions = True
    logging.config.dictConfig(cfg)


# from starlette.middleware.base import BaseHTTPMiddleware


# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# handler = LokiHandler(
#     url="http://127.0.0.1:3100/loki/api/v1/push",   # or http://loki:3100/... from inside Docker
#     version="1",
#     tags={"app": "pastebin-demo", "component": "fastapi"},
#     # If Loki multi-tenancy is enabled:
#     # headers={"X-Scope-OrgID": "1"},
# )
# logger = logging.getLogger("fastapi")
# logger.setLevel(logging.INFO)
# logger.addHandler(handler)

# class AccessLogMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         t0 = time.perf_counter()
#         response = await call_next(request)
#         logger.info(
#             "request",
#             extra={
#                 "tags": {"method": request.method, "path": request.url.path},
#                 "context": {
#                     "status": response.status_code,
#                     "duration_ms": round((time.perf_counter()-t0)*1000, 3),
#                     "client_ip": request.client.host if request.client else None,
#                 },
#             },
#         )
#         return response

def init_logger(app: FastAPI):
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        
        # Log request details
        logging.info(f"Request: Method: {request.method} Url: {request.url} - Headers: {request.headers}")
        
        # If you need to log the request body, you'll need to read it and then recreate it
        # as the request body can only be read once.
        # try:
        #     req_body = await request.json()
        #     logging.info(f"Request Body: {req_body}")
        # except Exception:
        #     pass # Handle cases where the request body is not JSON

        response = await call_next(request)
        
        end_time = time.time()
        process_time = round((end_time - start_time) * 1000) # in milliseconds

        # Log response details
        logging.info(f"Response: {response.status_code} - Processed in: {process_time}ms")
        
        # If you need to log the response body, you'll need to read it.
        # Note: Reading the response body here can be tricky with StreamingResponse or large responses.
        # It's generally safer to log specific headers or status codes.
        # try:
        #     res_body = await response.body()
        #     logging.info(f"Response Body: {res_body.decode()}")
        # except Exception:
        #     pass

        return response


__all__ = ["iniit_logger"]