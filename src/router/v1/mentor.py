import os
import time
import json
from typing import List, Dict, Any
from fastapi import (
    APIRouter,
    Request, Depends,
    Header, Path, Query, Body, Form
)
from ..res.response import *
from ...config.constant import *
from ...config.exception import *
import logging as log

log.basicConfig(filemode='w', level=log.INFO)


router = APIRouter(
    prefix='/users',
    tags=['Mentor'],
    responses={404: {'description': 'Not found'}},
)


@router.put('/{user_id}/mentor-profile',
            responses=post_response('upsert_mentor_profile', Any))
def upsert_mentor_profile(
    user_id: int = Path(...),
    body: Any = Body(...),
):
    # TODO: implement
    return res_success(data=None)


@router.get('/{user_id}/mentor-profile',
            responses=idempotent_response('get_mentor_profile', Any))
def get_mentor_profile(
    user_id: int = Path(...),
):
    # TODO: implement
    return res_success(data=None)


@router.put('/experiences/{experience_type}',
            responses=post_response('upsert_experience', Any))
def upsert_experience(
    experience_type: ExperienceCategory = Path(...),
    body: Any = Body(...),
):
    # TODO: implement
    return res_success(data=None)
