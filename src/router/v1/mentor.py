import os
import time
import json
from typing import List, Dict, Any
from fastapi import (
    APIRouter,
    Request, Depends,
    Header, Path, Query, Body, Form
)
from ...domain.mentor.model import (
    mentor_model as mentor,
    experience_model as experience,
)
from ...domain.user.model import (
    common_model as common,
)
from ..res.response import *
from ...config.conf import *
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
            responses=idempotent_response('upsert_mentor_profile', mentor.MentorProfileVO))
def upsert_mentor_profile(
    user_id: int = Path(...),
    body: mentor.MentorProfileDTO = Body(...),
):
    # TODO: implement
    return res_success(data=None)


@router.get('/{user_id}/mentor-profile',
            responses=idempotent_response('get_mentor_profile', mentor.MentorProfileVO))
def get_mentor_profile(
    user_id: int = Path(...),
):
    # TODO: implement
    return res_success(data=None)


@router.put('/{user_id}/experiences/{experience_type}',
            responses=idempotent_response('upsert_experience', experience.ExperienceVO))
def upsert_experience(
    user_id: int = Path(...),
    experience_type: ExperienceCategory = Path(...),
    body: experience.ExperienceDTO = Body(...),
):
    # TODO: implement
    return res_success(data=None)


@router.get('/expertises',
            responses=idempotent_response('get_expertises', common.ProfessionListVO))
def get_expertises(
    # category = ProfessionCategory.EXPERTISE
):
    # TODO: implement
    return res_success(data=None)


@router.get('/{user_id}/mentor-schedule',
            responses=idempotent_response('get_mentor_schedule', mentor.MentorScheduleVO))
def get_mentor_schedule(
    user_id: int = Path(...),
    year: int = Query(SCHEDULE_YEAR),
    batch: int = Query(BATCH),
    next_id: int = Query(0),
):
    # TODO: implement
    return res_success(data=None)


@router.put('/{user_id}/mentor-schedule',
            responses=idempotent_response('upsert_mentor_schedule', mentor.MentorScheduleVO))
def upsert_mentor_schedule(
    user_id: int = Path(...),
    body: List[mentor.TimeSlotDTO] = Body(...),
):
    # TODO: implement
    return res_success(data=None)
