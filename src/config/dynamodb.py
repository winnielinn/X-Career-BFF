import boto3
from .conf import TESTING, AWS_PROFILE
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


if TESTING == 'local':
    session = boto3.Session(profile_name=AWS_PROFILE)
else:
    session = boto3.Session()
dynamodb = session.resource('dynamodb')
