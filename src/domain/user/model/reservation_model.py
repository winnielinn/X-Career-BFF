import json
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel
from .user_model import *
from ....config.conf import *
from ....config.constant import *
import logging as log

log.basicConfig(filemode='w', level=log.INFO)


class UserDTO(BaseModel):
    user_id: int
    status: BookingStatus


class ReservationDTO(BaseModel):
    schedule_id: int
    mentor: UserDTO
    mentee: UserDTO
    start_datetime: int
    end_datetime: int
    message: Optional[str]


class ReservationVO(ReservationDTO):
    id: int


class ReservationListVO(BaseModel):
    reservations: List[ReservationVO]
    next_id: Optional[int]
