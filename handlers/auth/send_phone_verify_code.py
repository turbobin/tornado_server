# -*- coding: utf8 -*-
'''
发送验证码
'''
import random

from configs import err_conf
from handlers import BaseHandler
from utils import yd_qcloudsms, common


class Handle(BaseHandler):
    '''
    发送短信验证码
    '''

    def initialize(self):
        self.must_have_params = ['phone']
        self.db_handle = common.db_handle()
        self.template_id = 325316

    def send_verify_code(self, temp_code, params, phone, sms_sign):
        '''
        发送验证码
        '''
        yd_qcloudsms.yd_send_sms_param(temp_code, params, phone, sms_sign)

    def save_user_verify_code(self, phone, code):
        '''
        保存短信验证码
        '''
        content = "【验证码】WaterWorld 的验证码:{},请输入验证码完成帐号登录或注册。".format(code)
        sql = "insert into phone_code_tickets64 set phone=:phone, code=:code, content=:content"
        self.db_handle.query(sql, phone=phone, code=code, content=content)

    def post(self):
        '''
        处理请求
        '''
        phone = common.my_str(self.get_argument('phone'))
        is_right_phone = common.is_right_phone(phone)
        if not is_right_phone:
            return self.finish(common.Err(err_conf.E_BAD_PHONE))
        verify_code = random.randint(100000, 999999)
        params = []
        params.append(verify_code)
        sms_sign = "验证码"
        self.send_verify_code(self.template_id, params, phone, sms_sign)
        self.save_user_verify_code(phone, verify_code)
        response = common.Ok()
        return self.finish(response)
