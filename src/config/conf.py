import os
import json


XC_BUCKET = os.getenv('XC_BUCKET', 'x-career')

JWT_SECRET = os.getenv('JWT_SECRET', None)
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
TOKEN_EXPIRE_TIME = int(os.getenv('TOKEN_EXPIRE_TIME', 60 * 60 * 24 * 7))

BATCH = int(os.getenv('BATCH', '10'))

# schedule
SCHEDULE_YEAR = int(os.getenv('SCHEDULE_YEAR', '-1'))
SCHEDULE_MONTH = int(os.getenv('SCHEDULE_MONTH', '-1'))
SCHEDULE_DAY_OF_MONTH = int(os.getenv('SCHEDULE_DAY_OF_MONTH', '-1'))
SCHEDULE_DAY_OF_WEEK = int(os.getenv('SCHEDULE_DAY_OF_WEEK', '-1'))
