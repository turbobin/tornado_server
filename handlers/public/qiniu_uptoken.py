# coding:utf8
"""
获取七牛token
"""

from configs import err_conf
from handlers import BaseHandler
from utils import common, qiniu_tools


class QiniuTokenHandle(BaseHandler):
    """
    获取7牛token
    """

    def initialize(self):
        """
        初始化
        """
        self.must_have_params = ['user_id', 'business_source']
        self.LEGEL_BUSINESS_SOURCE = ['upload_exception']

    def post(self):
        """
        请求
        """
        business_source = common.my_str(self.get_argument('business_source'))
        if business_source not in self.LEGEL_BUSINESS_SOURCE:
            return self.finish(
                common.Err(err_conf.E_BAD_BUSINESS_SOURCE))
        filename = qiniu_tools.get_random_filename()
        up_token = qiniu_tools.get_up_token(business_source, filename)
        response = {
            'code': 0,
            'msg': 'ok',
            'up_token': up_token,
            'filename': filename
        }
        self.finish(response)
