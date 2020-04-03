from datetime import datetime
from urllib.parse import urlparse

import redis
import uvicorn
from fastapi import FastAPI, Query
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

import os

app = FastAPI()
db = redis.Redis(host= os.getenv('DB_HOST', 'localhost'))

# Override request validation exceptions to change default 'detail' to 'status'
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc) -> JSONResponse:
    return JSONResponse({"status": exc.detail})

@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request, exc) -> JSONResponse:
    return JSONResponse(content={"status": jsonable_encoder(exc.errors())})


@app.post("/visited_links")
def add_links(links: dict):
    if 'links' in links:
        for link in links['links']:
            clear_domain = urlparse(link).netloc or urlparse(link).path
            date = datetime.now().timestamp()
            data = f'{clear_domain}:{date}'
            try:
                db.zadd('linkHistory:domains', {data: date})
            except redis.exceptions.ConnectionError:
                return dict(status='На сервере неполадки с бд...')
    else:
        return dict(status='Массив ссылок отсутствует...')

    return dict(status = 'ok')

@app.get("/visited_domains")
def get_domains(date_start: int = Query(..., alias='from'), date_end: int = Query(..., alias='to')):
    answer = dict(domains=[], status='')
    if date_end - date_start < 0:
        answer['status'] = 'Некорректный интервал времени'
        return answer
    try:
        data = db.zrangebyscore('linkHistory:domains', date_start, date_end, withscores=True)
    except redis.exceptions.ConnectionError:
        return dict(status='На сервере неполадки с бд...')

    for item in data:
        answer["domains"].append(item[0].decode("utf-8").split(':')[0])
    answer["domains"] = sorted(set(answer["domains"]))
    answer["status"] = 'ok'

    return answer

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8080)
