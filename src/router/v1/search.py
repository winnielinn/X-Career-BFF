from typing import List, Dict, Any
from fastapi import (
    APIRouter,
    Request, Depends,
    Header, Path, Query, Body, Form
)
from ...domain.mentor.model import (
    mentor_model as mentor,
)
from ..res.response import *
from ...config.conf import *
from ...config.constant import *
from ...config.exception import *
import logging as log

log.basicConfig(filemode='w', level=log.INFO)


router = APIRouter(
    prefix='/mentors',
    tags=['Search Mentors'],
    responses={404: {'description': 'Not found'}},
)

@router.get('',
            responses=idempotent_response('mentor_list', Any))
def mentor_list(
    patterns: List[str] = Query(None),
    position: List[str] = Query(None),
    skill: List[str] = Query(None),
    topics: List[str] = Query(None),
    sorting: int = Query(0), # asc, desc
    next_id: int = Query(None),
):
    # TODO: implement
    return res_success(data=None)