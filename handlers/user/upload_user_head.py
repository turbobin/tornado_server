# coding:utf8
"""
上传用户头像
"""
from configs import err_conf
from handlers import BaseHandler
from handlers.user import user_handle
from utils import common


class Handle(BaseHandler):
    """
    上传用户头像
    """

    def initialize(self):
        """
        初始化
        """
        self.must_have_params = ['user_id', 'xyy']
        self.user_handle = user_handle.Handle()

    def post(self):
        """
        处理请求
        """
        file_metas = self.request.files['logo_file']
        user_id = common.my_int(self.get_argument('user_id', 0))
        filename = file_body = ""
        for meta in file_metas:
            filename = meta['filename']
            file_body = meta['body']
        if filename == "" or file_body == "":
            return self.finish(common.Err(err_conf.E_BAD_UPLOAD_HEAD))
        ret = self.user_handle.upload_head_url(user_id, file_body)
        head_url = ""
        if ret:
            head_url = common.get_user_head_url(user_id)
        return self.finish(dict(head_url=head_url))
