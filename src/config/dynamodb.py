import boto3
from .conf import AWS_PROFILE
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)



session = boto3.Session(profile_name=AWS_PROFILE)  # 指定所需的帳號
dynamodb = session.resource('dynamodb')
