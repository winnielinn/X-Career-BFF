#!/bin/bash

aws lambda update-function-configuration --function-name x-career-bff-dev-app --environment --profile xc "Variables={
STAGE=dev,
TESTING=dev,
XC_BUCKET=x-career,
REGION_HOST_AUTH=https://v0yqeljj19.execute-api.ap-northeast-1.amazonaws.com/dev/auth-service/api,
REGION_HOST_USER=https://gvjbxpuqmh.execute-api.ap-northeast-1.amazonaws.com/dev/user-service/api,
REGION_HOST_SEARCH=https://io9u1c6wah.execute-api.ap-northeast-1.amazonaws.com/dev/search-service/api,
JWT_ALGORITHM=HS256,
TOKEN_EXPIRE_TIME=30,
BATCH=10,
REQUEST_INTERVAL_TTL=8,
SHORT_TERM_TTL=1800,
LONG_TERM_TTL=259200,
TABLE_CACHE=dev_x_career_bff_cache,
SCHEDULE_YEAR=-1,
SCHEDULE_MONTH=-1,
SCHEDULE_DAY_OF_MONTH=-1,
SCHEDULE_DAY_OF_WEEK=-1
}"
