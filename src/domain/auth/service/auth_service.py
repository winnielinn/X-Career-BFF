from typing import Any, List, Dict
from ....router.req.authorization import gen_token
from ..model.auth_model import *
from ...cache import ICache
from ...service_api import IServiceApi
from ....infra.util.util import gen_confirm_code
from ....infra.util.time_util import gen_timestamp
from ....config.conf import *
from ....config.constant import PREFETCH
from ....config.exception import *
import logging as log

log.basicConfig(filemode='w', level=log.INFO)


class AuthService:
    def __init__(self, req: IServiceApi, cache: ICache):
        self.__cls_name = self.__class__.__name__
        self.req = req
        self.cache = cache

    '''
    signup
    '''

    async def signup(self, host: str, body: SignupDTO):
        email = body.email
        # TODO: not meta, check SignupDTO
        meta = body.meta
        self.__cache_check_for_duplicates(email)

        confirm_code = gen_confirm_code()
        auth_res = self.__req_send_confirmcode_by_email(
            host, email, confirm_code)

        if auth_res == 'email_sent':
            self.__cache_confirmcode(email, confirm_code, meta)

            # FIXME: remove the res here('confirm_code') during production
            return {
                'for_testing_only': confirm_code
            }

        else:
            self.cache.set(email, {'avoid_freq_email_req_and_hit_db': 1}, SHORT_TERM_TTL)
            raise DuplicateUserException(msg='email_registered')

    def __cache_check_for_duplicates(self, email: str):
        data = self.cache.get(email)
        if data:
            log.error(f'{self.__cls_name}.__cache_check_for_duplicates:[business error],\
                email:%s, cache data:%s', email, data)
            raise DuplicateUserException(msg='registered or registering')

    def __req_send_confirmcode_by_email(self, host: str, email: str, confirm_code: str):
        auth_res, msg, err = self.req.post(f'{host}/sendcode/email', json={
            'email': email,
            'confirm_code': confirm_code,
            'sendby': 'no_exist',  # email 不存在時寄送
        })
        
        if msg or err:
            log.error(f'{self.__cls_name}.__req_send_confirmcode_by_email:[request exception], \
                host:%s, email:%s, confirm_code:%s, auth_res:%s, msg:%s, err:%s',
                host, email, confirm_code, auth_res, msg, err)
            self.cache.set(email, {'avoid_freq_email_req_and_hit_db': 1}, SHORT_TERM_TTL)

        return auth_res

    def __cache_confirmcode(self, email: str, confirm_code: str, meta: str):
        email_playload = {
            'email': email,
            'confirm_code': confirm_code,
            # TODO: not meta, check SignupDTO
            'meta': meta,
        }
        self.cache.set(email, email_playload, ex=SHORT_TERM_TTL)

    '''
    confirm_signup
    '''

    async def confirm_signup(self, host: str, body: SignupConfirmDTO):
        email = body.email
        confirm_code = body.confirm_code
        user = self.cache.get(email)
        self.__verify_confirmcode(confirm_code, user)

        # 'registering': empty data, but TTL=30sec
        self.cache.set(email, {}, ex=30)
        auth_res = self.req.simple_post(f'{host}/signup',
                                        json={
                                            'email': email,
                                            # TODO: not meta, check SignupDTO
                                            'meta': user['meta'],
                                        })

        user_id_key = str(auth_res['user_id'])
        self.cache_auth_res(user_id_key, auth_res)
        auth_res = self.apply_token(auth_res)
        return {'auth': auth_res}

    def __verify_confirmcode(self, confirm_code: str, user: Any):
        if not user or not 'confirm_code' in user:
            raise NotFoundException(msg='no signup data')

        if user == {}:
            raise DuplicateUserException(msg='registering')

        if confirm_code != str(user['confirm_code']):
            raise ClientException(msg='wrong confirm_code')

    def apply_token(self, res: Dict):
        # gen jwt token
        token = gen_token(res, ['region', 'user_id'])
        res.update({'token': token})
        return res
    
    '''
    pre login API:
    
    若有機會在異地登入(不論是否真的在異地登入，因為無法確定)，則將登入流程改為 email 和 password 拆開：
    1. frontend: input `email`
    2. backend: gateway 直接訪問 S3, 取得該 email 的註冊地
        若在本地:
            則直接 `透過 auth service` 存取本地資料
        若在異地(如何確定在異地? gateway 需要知道 current_region)
            將資料 `透過 auth service` 從註冊地異步的複製到`目前所在地`
    3. frontend: input `password`
    4. backend: 若密碼正確則允許登入，可在`目前所在地`存取用戶資料
        此時不管用戶是否登入成功，該用戶資料早已 `透過 step 2` 複製到`目前所在地`
    5. 將 region (registration region) 緩存至手機或網頁(local storage)
        以便及早做 step 2 (在異地複製用戶資料)
    '''
    def login_preload(self, auth_host: str, user_host: str, body: LoginDTO):
        pass

    '''
    login
    有了 `login_preload`, login 可一律視為本地登入
    '''

    async def login(self, auth_host: str, user_host: str, body: LoginDTO):
        auth_res = self.__req_login(auth_host, body)

        # cache auth data
        user_id_key = str(auth_res['user_id'])
        self.cache_auth_res(user_id_key, auth_res)
        auth_res = self.apply_token(auth_res)

        # request user/professional data
        user_res = self.req_user_data(
            user_host,
            user_id_key,
            body.prefetch
        )

        return {
            'auth': auth_res,
            'user': user_res,
        }

    def __req_login(self, auth_host: str, body: LoginDTO):
        return self.req.simple_post(
            f'{auth_host}/login', json=body.dict())
        

    def cache_auth_res(self, user_id_key: str, auth_res: Dict):
        auth_res.update({
            'online': True,
        })
        updated = self.cache.set(
            user_id_key, auth_res, ex=LONG_TERM_TTL)
        if not updated:
            log.error(f'{self.__cls_name}.__cache_auth_res fail: [cache set],\
                user_id_key:%s, auth_res:%s, ex:%s, cache data:%s',
                user_id_key, auth_res, LONG_TERM_TTL, updated)
            raise ServerException(msg='server_error')

    def req_user_data(self, user_host: str, user_id_key: str, size: int = PREFETCH):            
        user_res = self.req.simple_get(
            url=f'{user_host}{user_id_key}/userdata',
            params={
                'size': size,
            }
        )

        return user_res

    '''
    logout
    '''

    async def logout(self, user_id: int):
        user_id_key = str(user_id)
        user = self.__cache_check_for_auth(user_id_key)
        user_logout_status = self.__logout_status(user)

        # 'LONG_TERM_TTL' for redirct notification
        self.__cache_logout_status(user_id_key, user_logout_status)
        return (None, 'successfully logged out')
    
    @staticmethod
    def is_login(cache: ICache, visitor: BaseAuthDTO = None) -> (bool):
        if visitor is None:
            return False

        user_id_key = str(visitor.user_id)
        user: Dict = cache.get(user_id_key)
        if user is None:
            return False

        return user.get('online', False)

    def __cache_check_for_auth(self, user_id_key: str):
        user = self.cache.get(user_id_key)
        if not user or not user.get('online', False):
            raise ClientException(msg='logged out')

        return user

    def __logout_status(self, user: Dict):
        user_id = user['user_id']
        region = user.get('region', None)

        return {
            'user_id': user_id,
            'region': region,
            'online': False,
        }

    def __cache_logout_status(self, user_id_key: str, user_logout_status: Dict):
        updated = self.cache.set(
            user_id_key, user_logout_status, ex=LONG_TERM_TTL)
        if not updated:
            log.error(f'{self.__cls_name}.__cache_logout_status fail: [cache set],\
                user_id_key:%s, user_logout_status:%s, ex:%s, cache data:%s',
                user_id_key, user_logout_status, LONG_TERM_TTL, updated)
            raise ServerException(msg='server_error')

    '''
    password
    '''
    async def send_reset_password_comfirm_email(self, auth_host: str, email: EmailStr):
        self.__cache_check_for_reset_password(email)
        data = self.__req_send_reset_password_comfirm_email(auth_host, email)
        self.__cache_token_by_reset_password(data['token'], email)
        #TEST: log
        return f'''send_email_success {data['token']}'''

    async def reset_passwrod(self, auth_host: str, verify_token: str, body: ResetPasswordDTO):
        checked_email = self.cache.get(verify_token)
        if not checked_email:
            raise UnauthorizedException(msg='invalid token') 
        if checked_email != body.register_email:
            raise UnauthorizedException(msg='invalid user')
        self.__req_reset_password(auth_host, body)
        self.__cache_remove_by_reset_password(verify_token, checked_email)

    
    def __cache_check_for_reset_password(self, email: EmailStr):
        data = self.cache.get(f'{email}:reset_pw')
        if data:
            log.error(f'{self.__cls_name}.__cache_check_for_reset_password:[too many reqeusts error],\
                email:%s, cache data:%s', email, data)
            raise TooManyRequestsException(msg='frequent_requests')
    
    def __cache_token_by_reset_password(self, verify_token: str, email: EmailStr):
        self.cache.set(f'{email}:reset_pw', '1', REQUEST_INTERVAL_TTL)
        self.cache.set(verify_token, email, SHORT_TERM_TTL)
        
    def __cache_remove_by_reset_password(self, verify_token: str, email: EmailStr):
        self.cache.delete(f'{email}:reset_pw')
        self.cache.delete(verify_token)
        

    async def update_password(self, auth_host: str, user_id: int, body: UpdatePasswordDTO):
        self.__cache_check_for_email_validation(user_id, body.register_email)
        self.__req_update_password(auth_host, body)

    def __req_send_reset_password_comfirm_email(self, auth_host: str, email: EmailStr):
        return self.req.simple_get(
            f'{auth_host}/password/reset/email', params={'email': email}) 

    def __cache_check_for_email_validation(self, user_id: int, register_email: EmailStr):
        user_id_key = str(user_id)
        data = self.cache.get(user_id_key)
        if not 'email' in data or str(register_email) != data['email']:
            raise UnauthorizedException(msg='invalid email')

    def __req_update_password(self, auth_host: str, body: UpdatePasswordDTO):
        return self.req.simple_put(
            f'{auth_host}/password/update', json=body.dict())

    def __req_reset_password(self, auth_host: str, body: ResetPasswordDTO):
        return self.req.simple_put(
            f'{auth_host}/password/update', json=body.dict()) 