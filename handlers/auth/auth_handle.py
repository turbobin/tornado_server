# -*- coding: utf8 -*-

import sys

sys.path.append("../..")
import hashlib
from utils import common, queue_tools
import random, string
from configs import config


class Handle():
    def __init__(self):
        self.db_handle = common.db_handle()
        self.db1_handle = common.db1_handle()
        self.db_redis = common.redis_handle()
        self.queue_handle = queue_tools.Handle()

    def genarate_access_token(self, string_token):
        """生成token"""
        access_token = hashlib.md5(string_token.encode("utf-8")).hexdigest()
        return access_token

    def genarate_session_key(self, length=64):
        """生成一个随机的session key"""
        # 数字的个数随机产生
        num_of_numeric = random.randint(1, length - 1)
        # 剩下的都是字母
        num_of_letter = length - num_of_numeric
        # 随机生成数字
        numerics = [random.choice(string.digits) for _ in range(num_of_numeric)]
        # 随机生成字母
        letters = [random.choice(string.ascii_letters) for _ in range(num_of_letter)]
        # 结合两者
        all_chars = numerics + letters
        # 洗牌
        random.shuffle(all_chars)
        # 生成最终字符串
        session_key = ''.join([i for i in all_chars])
        return session_key

    def get_user_session_key(self, user_id):
        """获取session key"""
        key = "session_key_{}".format(user_id)
        session_key = common.my_str(self.db_redis.get(key))
        if not session_key:
            session_key = self.genarate_session_key()
            self.db_redis.set(key, session_key, ex=7 * 86400)
        ttl = self.db_redis.ttl(key)
        return session_key, ttl

    def bind_phone(self, user_id, phone):
        """绑定手机号操作"""
        sql = """
        update user_info set phone=:phone where user_id=:user_id
        """
        self.db_handle.query(sql, phone=phone, user_id=user_id)

    def get_user_id_by_phone(self, phone):
        """根据手机号获取user_id"""
        sql = "select user_id from user_info where phone=:phone and status=0"
        result = self.db_handle.query(sql, phone=phone)
        return result[0].user_id if result.first() else 0

    def save_wechat_openid_info(self, args):
        """保存微信授权登录的信息"""
        sql = """
        insert into openid_info set open_id=:open_id, source=:source, user_id=:user_id,
        status=:status, nick=:nick, sex=:sex, head_url=:head_url, union_id=:union_id,
        type=:type on duplicate key update
        source=:source, user_id=:user_id, status=:status, nick=:nick, sex=:sex,
        head_url=:head_url, union_id=:union_id
        """
        self.db_handle.query(sql, **args)

    def get_user_id_by_openid(self, openid):
        """通过open_id 获取 user_id"""
        sql = """
        select user_id from openid_info where open_id=:open_id
        """
        result = self.db_handle.query(sql, open_id=openid)
        return result[0].user_id if result.first() else 0

    def get_phone_by_user_id(self, user_id):
        """通过user_id 获取手机号"""
        sql = """
        select phone from user_info where user_id=:user_id and status=0
        """
        result = self.db_handle.query(sql, user_id=user_id)
        return result[0].phone if result.first() else ''

    def register_user(self, request, data):
        """用户注册"""
        ip = request.headers.get('X-Real-Ip', '')
        if ip == "":
            ip = request.remote_ip
        user_id = self._genarate_new_user_id()
        nick = data.get('nick', '用户{}'.format(user_id))
        sex = data.get('sex', 0)
        head_url = data.get('head_url', config.DEFAULT_HEAD_URL)
        phone = data.get('phone', '')
        source = data.get('source', '')
        phone_type = data.get('phone_type', '')
        os = data.get('os', '')
        ver = data.get('ver', '')
        channel = data.get('channel', '')
        device_id = data.get('device_id', '')

        self.deal_with_head_url(user_id, head_url)
        if nick == "":
            nick = "用户{0}".format(user_id)
        args = dict(
            user_id=user_id,
            phone=phone,
            nick=nick,
            sex=sex,
            source=source,
            ip=ip,
            phone_type=phone_type,
            os=os,
            ver=ver,
            channel=channel,
            device_id=device_id
        )
        sql = '''insert into user_info set user_id=:user_id,phone=:phone,nick=:nick,sex=:sex,
        source=:source,ip=:ip,reg_ts=now(),phone_type=:phone_type,os=:os,ver=:ver,channel=:channel,
        device_id=:device_id,last_login_ts=now() '''
        self.db_handle.query(sql, **args)
        return user_id

    def update_user_info(self, request, data):
        """重新登录更新用户信息"""
        ip = request.headers.get('X-Real-Ip', '')
        if ip == "":
            ip = request.remote_ip
        user_id = data['user_id']  # data中必须包含user_id
        nick = data.get('nick', '悦友{}'.format(user_id))
        sex = data.get('sex', 0)
        head_url = data.get('head_url', config.DEFAULT_HEAD_URL)
        phone = data.get('phone', '')
        source = data.get('source', '')
        phone_type = data.get('phone_type', '')
        os = data.get('os', '')
        ver = data.get('ver', '')
        channel = data.get('channel', '')
        device_id = data.get('device_id', '')

        self.deal_with_head_url(user_id, head_url)
        args = dict(
            user_id=user_id,
            phone=phone,
            nick=nick,
            sex=sex,
            source=source,
            ip=ip,
            phone_type=phone_type,
            os=os,
            ver=ver,
            channel=channel,
            device_id=device_id
        )
        sql = '''
        update user_info set phone=:phone,nick=:nick,sex=:sex,
        source=:source,ip=:ip,reg_ts=now(),phone_type=:phone_type,os=:os,ver=:ver,channel=:channel,
        device_id=:device_id,last_login_ts=now() where user_id=:user_id'''
        self.db_handle.query(sql, **args)

    def deal_with_head_url(self, user_id, head_url):
        '''
        后续处理
        '''
        task_name = "wwd_upload_head_url"
        job_data = {"head_url": head_url}
        self.queue_handle.add_to_queue(user_id, task_name, job_data)

    def _genarate_new_user_id(self):
        sql = "insert into user_tickets64_innodb () values()"
        self.db1_handle.query(sql)
        sql = 'select last_insert_id() as id'
        result = self.db1_handle.query(sql)
        return result[0].id


if __name__ == '__main__':
    handle = Handle()
    print(handle.genarate_session_key())
