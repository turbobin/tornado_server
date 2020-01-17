# -*- coding: utf8 -*-
"""
获取用户信息
"""

from configs import err_conf
from handlers import BaseHandler
from utils import common
from handlers.user import user_handle


class Handle(BaseHandler):
    """
    获取用户信息
    """

    def initialize(self):
        self.must_have_params = ['user_id', 'xyy']
        self.user_handle = user_handle.Handle()

    def post(self):
        user_id = common.my_int(self.get_argument('user_id'))
        xyy = common.my_str(self.get_argument("xyy"))
        if not common.check_user_sid(user_id, xyy):
            return self.finish(common.Err(err_conf.E_BAD_XYY))
        user_info = self.user_handle.get_user_info(user_id)
        response = dict(code=0, msg="ok", user_info=user_info)
        return self.finish(response)


if __name__ == "__main__":
    import unit_test
    data = dict(
        user_id=255495082,
        xyy="25ab6695889381c9476ac31e6b3b6c4f"
    )
    unit_test.execute(data, "/user/get_user_info", port=5001)
