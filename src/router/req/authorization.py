import os
import time
from datetime import datetime
from typing import Callable, List, Union, Dict
import jwt as jwt_util
from fastapi import APIRouter, FastAPI, Header, Path, Query, Body, Request, Response, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.routing import APIRoute
from ...config.conf import JWT_SECRET, JWT_ALGORITHM, TOKEN_EXPIRE_TIME
from ...config.exception import *
import logging as log

log.basicConfig(level=log.INFO)

auth_scheme = HTTPBearer()

# token required in Header
def token_required(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    pass

def parse_token(credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    if not token:
        log.error(f'parse_token fail: [\'token\' is required in credentials], credentials:{credentials}')
        raise UnauthorizedException(msg='Authorization failed')
    
    return token

async def parse_token_from_request(request: Request):
    credentials: HTTPAuthorizationCredentials = await auth_scheme.__call__(request)
    if not credentials:
        raise UnauthorizedException(msg='Authorization header missing')
    
    return parse_token(credentials)


def __get_secret(user_id):
    return f'secret{str(user_id)[::-1]}' # if user_id != None else JWT_SECRET

def gen_token(data: dict, fields: List):
    public_info = {}
    if not 'user_id' in data:
        log.error(f'gen_token fail: [\'user_id\' is required in data], data:{data}, fields:{fields}')
        raise ServerException(msg='internal server error')
    
    secret = __get_secret(data['user_id'])
    for field in fields:
        val = str(data[field])
        public_info[field] = val
        
    exp = datetime.now().timestamp() + TOKEN_EXPIRE_TIME
    public_info.update({ 'exp': exp })
    return jwt_util.encode(payload=public_info, key=secret, algorithm=JWT_ALGORITHM)


def get_user_id(url_path: str) -> (int):
    try:
        # TODO: define how to parse user_id from url_path
        return int(url_path.split('/')[6])
    except Exception as e:
        log.error(f'cannot get user_id from url path, url_path:{url_path}, err:{e}')
        raise NotFoundException(msg='\'user_id\' is not found in url path')


def __jwt_decode(jwt, key, msg):
    try:
        algorithms = [JWT_ALGORITHM]
        return jwt_util.decode(jwt, key, algorithms)
    except Exception as e:
        log.error(f'__jwt_decode fail, key:{key}, algorithms:{algorithms}, msg:{msg}, jwt:{jwt}, \ne:{e}')
        raise UnauthorizedException(msg=msg)


def __valid_user_id(data: dict, user_id):
    if not 'user_id' in data:
        return False

    return int(data['user_id']) == int(user_id)



def __verify_token_in_auth(user_id: int, credentials: HTTPAuthorizationCredentials, err_msg: str):
    secret = __get_secret(user_id)
    token = parse_token(credentials)
    data = __jwt_decode(jwt=token, key=secret, msg=err_msg)
    if not __valid_user_id(data, user_id):
        raise UnauthorizedException(msg=err_msg)


async def verify_token(request: Request):
    url_path = request.url.path
    user_id = get_user_id(url_path)
    
    token = await parse_token_from_request(request)
    secret = __get_secret(user_id)
    data = __jwt_decode(jwt=token, key=secret, msg=f'invalid user')
    if not __valid_user_id(data, user_id):
        raise UnauthorizedException(msg=f'invalid user')


def verify_token_by_update_password(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
                                    role_id: int = Path(...),
                                    ):
    __verify_token_in_auth(role_id, credentials, "access denied")


class AuthRoute(APIRoute):
    def get_route_handler(self) -> (Callable):
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            
            await verify_token(request)
            
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers['X-Response-Time'] = str(duration)
            log.info(f'route duration: {duration}')
            log.info(f'route response headers: {response.headers}')
            # log.info(f'route response: {response}')
            return response

        return custom_route_handler
