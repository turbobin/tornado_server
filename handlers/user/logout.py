# -*- coding: utf8 -*-
"""
账号注销
"""

from handlers import BaseHandler
from handlers.user import user_handle
from utils import common


class Handle(BaseHandler):
    """
    账号注销操作
    """

    def initialize(self):
        self.must_have_params = ['user_id', 'xyy']
        self.user_handle = user_handle.Handle()

    def post(self):
        """
        1. 更改用户状态为删除
        2. 解除绑定open_id
        3. 清除登录态
        """
        user_id = common.my_int(self.get_argument('user_id'))

        args = dict(user_id=user_id, status=9)
        self.user_handle.update_user_info(args)

        self.user_handle.unbind_user_opendid_info(user_id)
        common.remove_user_sid(user_id)
