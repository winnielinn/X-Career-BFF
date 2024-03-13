import json
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel
from ....config.constant import *
import logging as log

log.basicConfig(filemode='w', level=log.INFO)


class InterestVO(BaseModel):
    category: InterestCategory
    subject: str
    desc: Dict


class InterestListVO(BaseModel):
    interests: List[InterestVO] = []


class ProfessionVO(BaseModel):
    category: ProfessionCategory
    subject: str
    metadata: Dict


class ProfessionListVO(BaseModel):
    professions: List[ProfessionVO] = []
