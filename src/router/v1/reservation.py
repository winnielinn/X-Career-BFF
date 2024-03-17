from typing import List, Dict, Any
from fastapi import (
    APIRouter,
    Request, Depends,
    Header, Path, Query, Body, Form
)
from ...domain.reservation.model import (
    reservation_model as reservation,
)
from ..res.response import *
from ...config.conf import *
from ...config.constant import *
from ...config.exception import *
import logging as log

log.basicConfig(filemode='w', level=log.INFO)


router = APIRouter(
    prefix='/reservations',
    tags=['Reservations'],
    responses={404: {'description': 'Not found'}},
)


@router.get('',
            responses=idempotent_response('reservation_list', reservation.ReservationListVO))
def reservation_list(
    state: ReservationListState = Query(...),
    batch: int = Query(...),
    next_id: int = Query(None),
):
    # TODO: implement
    return res_success(data=None)


@router.post('',
             responses=post_response('new_booking', reservation.ReservationVO))
def new_booking(
    body: List[reservation.ReservationDTO] = Body(...),
):
    # TODO: implement
    return res_success(data=None)


@router.put('/{reservation_id}',
            responses=idempotent_response('update_or_delete_booking', reservation.ReservationVO))
def update_or_delete_booking(
    reservation_id: int,
    body: List[reservation.ReservationDTO] = Body(...),
):
    # TODO: implement
    return res_success(data=None)
