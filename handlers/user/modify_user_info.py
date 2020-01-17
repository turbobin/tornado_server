# -*- coding: utf8 -*-
"""
修改用户信息
"""

from handlers import BaseHandler
from handlers.user import user_handle
from utils import common


class Handle(BaseHandler):
    """
    修改用户信息
    """

    def initialize(self):
        self.must_have_params = ['user_id', 'xyy']
        self.user_handle = user_handle.Handle()

    def post(self):
        user_id = common.my_int(self.get_argument('user_id'))

        sex = common.my_int(self.get_argument('sex', None))
        height = common.my_int(self.get_argument('height', None))
        weight = common.my_int(self.get_argument('weight', None))
        nick = common.my_str(self.get_argument('nick', None))
        birthday = common.my_int(self.get_argument('birthday', None))
        blood_type = common.my_str(self.get_argument('blood_type', None))
        blood_pressure = common.my_str(self.get_argument('blood_pressure', None))
        heart_rate = common.my_int(self.get_argument('heart_rate', None))
        blood_sugar = common.my_int(self.get_argument('blood_sugar', None))

        args = dict(
            user_id=user_id,
            nick=common.text_filter(nick),
            sex=sex,
            height=height,
            weight=weight,
            birthday=birthday,
            blood_pressure=blood_pressure,
            blood_sugar=blood_sugar,
            blood_type=blood_type,
            heart_rate=heart_rate
        )
        self.user_handle.update_user_info(args)

        return self.finish(common.Ok())
