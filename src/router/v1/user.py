import os
import time
import json
from typing import List, Dict, Any
from fastapi import (
    APIRouter,
    Request, Depends,
    Header, Path, Query, Body, Form
)
from ...domain.user.model import (
    common_model as common,
    user_model as user,
)
from ..res.response import *
from ...config.constant import *
from ...config.exception import *
import logging as log

log.basicConfig(filemode='w', level=log.INFO)


router = APIRouter(
    prefix='/users',
    tags=['Profile'],
    responses={404: {'description': 'Not found'}},
)


@router.put('/{user_id}/profile',
            responses=idempotent_response('upsert_profile', user.ProfileVO))
def upsert_profile(
    user_id: int = Path(...),
    body: user.ProfileDTO = Body(...),
):
    # TODO: implement
    return res_success(data=None)


@router.get('/{user_id}/profile',
            responses=idempotent_response('get_profile', user.ProfileVO))
def get_profile(
    user_id: int = Path(...),
):
    # TODO: implement
    return res_success(data=None)


@router.get('/interests',
            responses=idempotent_response('get_interests', common.InterestListVO))
def get_interests(
    interest: InterestCategory = Query(...),
):
    # TODO: implement
    return res_success(data=None)


@router.get('/professions',
            responses=idempotent_response('get_professions', common.ProfessionListVO))
def get_professions(
    profession: ProfessionCategory = Query(...),
):
    # TODO: implement
    return res_success(data=None)
