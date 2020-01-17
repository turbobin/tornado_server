# -*- coding: utf8 -*-
"""
绑定手机号
"""

from handlers.auth import auth_handle
from utils import common
from handlers import BaseHandler


class Handle(BaseHandler):
    """
    绑定手机号
    """

    def initialize(self):
        """
        初始化
        """
        self.must_have_params = ['user_id', 'access_token', 'phone']
        self.auth_handle = auth_handle.Handle()
        self.db_redis = common.redis_handle()

    def post(self):
        """
        处理请求
        """
        user_id = common.my_int(self.get_argument('user_id'))
        phone = common.my_str(self.get_argument('phone'))
        access_token = common.my_str(self.get_argument('access_token'))
        user_phone = self.db_redis.get(access_token)
        if user_phone != phone:
            return self.finish(common.Err("无效的token或手机号!"))
        bind_user_id = self.auth_handle.get_user_id_by_phone(phone)
        if user_id != bind_user_id:
            return self.finish(common.Err("当前手机号已经绑定其他的微信/QQ账号!"))
        self.auth_handle.bind_phone(user_id, phone)
        return self.finish(common.Ok())
