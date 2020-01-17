# -*- coding: utf8 -*-
"""
微信登陆
"""

import requests

from configs import err_conf, config
from handlers import BaseHandler
from handlers.auth import auth_handle
from utils import common
from utils.log import send_try_except


class Handle(BaseHandler):

    def initialize(self):
        """
        初始化
        """
        self.must_have_params = ['code']
        self.auth_handle = auth_handle.Handle()

    def auth_of_wechat(self, code):
        """
        微信认证
        """
        response_info = {}
        url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}&secret={1}&grant_type=authorization_code".format(
            config.WECHAT_APP_ID, config.WECHAT_APP_SECRET, code)
        try:
            response = requests.get(url)
            response_info = response.json()
        except Exception:
            send_try_except()
        return response_info

    def query_user_info(self, open_id, access_token, refresh_token):
        """
        获取用户的信息
        """
        response_info = {}
        url = "https://api.weixin.qq.com/sns/userinfo?access_token={0}&openid={1}".format(
            access_token, open_id)
        try:
            response = requests.get(url)
            response_info = response.json()
            if 'errcode' in response_info:
                return None
        except Exception:
            send_try_except()
        return response_info

    def post(self):
        """
        处理请求
        """
        code = common.my_str(self.get_argument('code'))
        response_info = self.auth_of_wechat(code)
        if not response_info:
            return self.finish(common.Err(err_conf.E_BAD_WX_AUTH))
        open_id = response_info['openid']
        access_token = response_info['access_token']
        refresh_token = response_info['refresh_token']
        response_info = self.query_user_info(open_id, access_token, refresh_token)
        if not response_info:
            return self.finish(common.Err(err_conf.E_BAD_WX_AUTH))
        union_id = response_info.get('unionid', '')
        head_url = response_info.get('headimgurl', '')
        nick = response_info.get('nickname', '')
        sex = response_info.get('sex', 0)  # 1是男性，2是女性，0是未知
        is_bind_phone = 0
        # 检查是否有user_id
        user_id = self.auth_handle.get_user_id_by_openid(open_id)
        data = {k: v[0].decode('utf-8') for k, v in self.request.arguments.items()}
        data.update({"sex": sex, "head_url": head_url, "nick": nick})
        if user_id > 0:
            phone = self.auth_handle.get_phone_by_user_id(user_id)
            is_bind_phone = 1 if phone else 0
            data.update({"user_id": user_id, "phone": phone})
            self.auth_handle.update_user_info(self.request, data)
        else:
            user_id = self.auth_handle.register_user(self.request, data)

        args = {
            "opend_id": open_id,
            "user_id": user_id,
            "source": self.get_argument("source", ""),
            "nick": nick,
            "sex": sex,
            "head_url": head_url,
            "status": 0,
            "union_id": union_id,
            "type": 2
        }
        self.auth_handle.save_wechat_openid_info(args)
        xyy = common.get_user_sid(user_id)
        session_key, ttl = self.auth_handle.get_user_session_key(user_id)
        response = {
            "code": 0,
            "msg": "ok",
            "session_key": session_key,
            "ttl": ttl,
            "is_bind_phone": is_bind_phone,
            "user_info": {
                "user_id": user_id,
                "nick": nick,
                "head_url": head_url,
                "xyy": xyy
            }
        }
        return self.finish(response)
