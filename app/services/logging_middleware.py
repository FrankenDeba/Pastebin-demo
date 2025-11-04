# logging_middleware.py
import time, json, logging
from typing import Optional
from fastapi import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("app")

SECRET_KEYS = {"password", "passwd", "secret", "token", "authorization", "api_key", "apikey", "access_token"}

def _mask_json_text(text: str) -> str:
    try:
        data = json.loads(text)
        def mask(v):
            if isinstance(v, dict):
                return {k: ("***" if k.lower() in SECRET_KEYS else mask(vv)) for k, vv in v.items()}
            if isinstance(v, list):
                return [mask(x) for x in v]
            return v
        return json.dumps(mask(data), ensure_ascii=False)
    except Exception:
        return text

class RequestResponseLoggerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, body_limit: int = 1000) -> None:
        super().__init__(app)
        self.body_limit = body_limit

    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()

        # --- capture request body (and keep it available downstream) ---
        try:
            req_bytes = await request.body()
            req_text = _mask_json_text(req_bytes.decode("utf-8", errors="replace"))[:self.body_limit]
        except Exception:
            req_text = None

        # --- call downstream and capture response body ---
        response = await call_next(request)

        resp_bytes = b""
        try:
            async for chunk in response.body_iterator:
                resp_bytes += chunk
        except Exception:
            pass  # streaming/exception responses may not iterate cleanly

        # Rebuild response so Content-Length is correct (prevents your error)
        headers = dict(response.headers)
        # Starlette will set the correct content-length; we can drop the old one
        headers.pop("content-length", None)
        new_response = Response(
            content=resp_bytes,
            status_code=response.status_code,
            headers=headers,
            media_type=getattr(response, "media_type", None),
            background=getattr(response, "background", None),
        )

        # --- labels (low cardinality) ---
        route_tmpl = getattr(request.scope.get("route"), "path", request.url.path)
        logger.info(
            "HTTP request/response",
            extra={"tags": {
                "service": "api",
                "method": request.method,
                "route": route_tmpl,
                "status": str(response.status_code),
            }},
        )

        # --- detailed JSON payload (parse with `| json` in Loki) ---
        detail = {
            "event": "http_access",
            "method": request.method,
            "route": route_tmpl,
            "path": request.url.path,
            "status": response.status_code,
            "duration_ms": int((time.perf_counter() - start) * 1000),
            "client_ip": request.client.host if request.client else None,
            "user_agent": request.headers.get("user-agent"),
            "request_body": req_text,
            "response_body": _mask_json_text(resp_bytes.decode("utf-8", errors="replace"))[:self.body_limit] if resp_bytes else None,
        }
        logger.info(json.dumps(detail, ensure_ascii=False))

        return new_response
