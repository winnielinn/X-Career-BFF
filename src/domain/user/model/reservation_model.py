import json
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel
from .user_model import *
from ....config.conf import *
from ....config.constant import *
import logging as log

log.basicConfig(filemode='w', level=log.INFO)


class UserStatusDTO(BaseModel):
    user_id: int
    status: BookingStatus


class ReservationDTO(BaseModel):
    schedule_id: int
    mentor: UserStatusDTO
    mentee: UserStatusDTO
    start_datetime: int
    end_datetime: int
    message: Optional[str]


class AsyncUserDataVO(UserStatusDTO):
    name: Optional[str]
    avator: Optional[str]
    position: Optional[str]
    company: Optional[str]
    industry: Optional[ProfessionVO]
    role: Optional[RoleType]


class ReservationVO(BaseModel):
    id: int
    schedule_id: int
    participant: AsyncUserDataVO
    my_status: BookingStatus
    start_datetime: int
    end_datetime: int
    message: Optional[str]


class ReservationListVO(BaseModel):
    reservations: List[ReservationVO]
    next_id: Optional[int]
