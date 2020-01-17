# -*- coding: utf8 -*-
"""
手机号注册登录
"""

from handlers.auth import auth_handle
from handlers import BaseHandler
from utils import common


class Handle(BaseHandler):
    """
    手机号注册登陆
    """

    def initialize(self):
        self.must_have_params = ['phone', 'access_token']
        self.auth_handle = auth_handle.Handle()
        self.db_redis = common.redis_handle()

    def post(self):
        phone = common.my_str(self.get_argument('phone'))
        access_token = common.my_str(self.get_argument('access_token'))

        user_phone = common.my_str(self.db_redis.get(access_token))
        if user_phone != phone:
            return self.finish(common.Err("无效的token或手机号!"))

        user_id = self.auth_handle.get_user_id_by_phone(phone)
        if user_id > 0:
            self.auth_handle.bind_phone(user_id, phone)
        else:
            data = {k: v[0].decode('utf-8') for k, v in self.request.arguments.items()}
            user_id = self.auth_handle.register_user(self.request, data)

        xyy = common.get_user_sid(user_id)
        session_key, ttl = self.auth_handle.get_user_session_key(user_id)
        response = {
            "code": 0,
            "msg": "ok",
            "session_key": session_key,
            "ttl": ttl,
            "user_info": {
                "user_id": user_id,
                "xyy": xyy
            }
        }
        return self.finish(response)
