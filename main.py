import os
from mangum import Mangum
from fastapi import FastAPI, Request, \
    Header, Path, Query, Body, Form, \
    File, UploadFile, status, \
    HTTPException, \
    Depends, \
    APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.router.v1 import (
    account,
    user,
    mentor,
    search,
    reservation,
)
from src.config import exception

STAGE = os.environ.get('STAGE')
root_path = '/' if not STAGE else f'/{STAGE}'
app = FastAPI(title='X-Career: BFF', root_path=root_path)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

router_v1 = APIRouter(prefix='/api/v1')
router_v1.include_router(account.router)
router_v1.include_router(user.router)
router_v1.include_router(mentor.router)
router_v1.include_router(search.router)
router_v1.include_router(reservation.router)

app.include_router(router_v1)

exception.include_app(app)


@app.get('/gateway/{term}')
async def info(term: str):
    if term != 'yolo':
        raise HTTPException(
            status_code=418, detail='Oops! Wrong phrase. Guess again?')
    return JSONResponse(content={'mention': 'You only live once.'})

# Mangum Handler, this is so important
handler = Mangum(app)
