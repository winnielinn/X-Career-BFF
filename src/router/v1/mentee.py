import os
import time
import json
from typing import List, Dict, Any
from fastapi import APIRouter, \
    Request, Depends, \
    Cookie, Header, Path, Query, Body, Form
from ..res.response import *
from ...config.exception import *
import logging as log

log.basicConfig(filemode='w', level=log.INFO)


router = APIRouter(
    prefix='/mentees',
    tags=['Mentee'],
    responses={404: {'description': 'Not found'}},
)