# -*- coding: utf8 -*-
"""
校验手机号
"""

import time

from handlers.auth import auth_handle
from configs import err_conf
from handlers import BaseHandler
from utils import common


class Handle(BaseHandler):
    """
    校验手机号
    """

    def initialize(self):
        self.must_have_params = ['phone', 'app_package', 'verify_code']
        self.db_handle = common.db_handle()
        self.db_redis = common.redis_handle()
        self.auth_handle = auth_handle.Handle()

    def post(self):
        """
        处理请求参数
        """
        phone = common.my_str(self.get_argument('phone'))
        app_package = common.my_str(self.get_argument('app_package'))
        verify_code = common.my_int(self.get_argument('verify_code'))
        is_right_phone = common.is_right_phone(phone)
        if not is_right_phone:
            return self.finish(err_conf.E_BAD_PHONE)
        sms_code=0
        now=int(time.time())
        send_ts=0
        sql="""select code, unix_timestamp(ts) as ts from phone_code_tickets64
        where phone={0} order by ts desc limit 1""".format(int(phone))
        result=self.db_handle.query(sql)
        for item in result:
            sms_code=item.code
            send_ts=item.ts
        if verify_code != sms_code:
            return self.finish(common.Err(err_conf.E_BAD_CHECK_PHONE_CODE))
        # 验证码5分钟内有效
        if now - send_ts > 5 * 60:
            return self.finish(common.Err(err_conf.E_PHONE_CODE_EXPIRE))

        # 生成token
        string_token="{0}{1}{2}".format(phone, app_package, now)
        access_token = self.auth_handle.genarate_access_token(string_token)
        self.db_redis.set(access_token, phone, ex = 5*60)
        response={'code': 0, 'msg': 'ok', "access_token": access_token}
        return self.finish(response)
