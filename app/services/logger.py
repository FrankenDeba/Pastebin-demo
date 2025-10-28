from fastapi import FastAPI, Request, Response

import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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