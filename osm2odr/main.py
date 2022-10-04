import time
from uuid import uuid4 as uid

from fastapi import FastAPI, Request

from osm2odr.api import api
from osm2odr.core.logging import log


app = FastAPI()
app.include_router(api)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    c_id = uid().hex
    log.info(f"id={c_id} start request path={request.url.path}")

    start_time = time.time()
    resp = await call_next(request)
    process_time = (time.time() - start_time) * 1000

    fmt_process_time = '{0:.2f}'.format(process_time)
    log.info(f"id={c_id} completed_in={fmt_process_time}ms status_code={resp.status_code}")
    resp.headers["X-Process-Time"] = str(process_time)

    return resp
