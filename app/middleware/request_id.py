from uuid import uuid4
from fastapi import Request, Response
from app.core.request_context import request_id_ctx_var

async def request_id_middleware(request: Request, call_next):
    rid = request.headers.get("X-Request-ID") or str(uuid4())
    token = request_id_ctx_var.set(rid)
    try:
        response: Response = await call_next(request)
        response.headers["X-Request-ID"] = rid
        return response
    finally:
        request_id_ctx_var.reset(token)
