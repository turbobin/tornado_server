# -*- coding: utf8 -*-
"""
获取session_key
"""

from handlers.auth import auth_handle
from handlers import BaseHandler
from utils import common


class Handle(BaseHandler):
    """
    获取session_key
    """

    def initialize(self):
        self.must_have_params = ['user_id', 'xyy']
        self.auth_handle = auth_handle.Handle()

    def post(self):
        user_id = common.my_int(self.get_argument("user_id", 0))
        session_key, ttl = self.auth_handle.get_user_session_key(user_id)
        response = dict(code=0, msg="ok", session_key=session_key, ttl=ttl)
        return self.finish(response)
