# -*- coding: utf8 -*-
import sys

sys.path.append("..")
import os
import stat
import time
from io import BytesIO
from PIL import Image
from utils import common
from utils.log import send_try_except
from utils import qiniu_tools
from configs import config


class Handle():
    def __init__(self):
        self.db_handle = common.db_handle()
        self.redis_handle = common.redis_handle()
        self.db_columns = {
            "user_id", "sex", "nick", "rank", "height", "weight",
            "blood_type", "blood_pressure", "blood_sugar", "heart_rate",
            "phone", "birthday", "unix_timestamp(reg_ts) as reg_ts", "status"
        }
        self.columns = ",".join(self.db_columns)

    def get_user_info(self, user_id):
        """获取用户信息"""
        sql = "select {columns} from user_info where user_id=:user_id and status=0".format(
            columns=self.columns)
        result = self.db_handle.query(sql, user_id=user_id)
        user_info = result.first(as_dict=True)
        if user_info:
            user_info["head_url"] = common.get_user_head_url(user_id)
        return user_info

    def update_user_info(self, args):
        """修改用户信息"""
        format_columns = ""
        for k, v in args:
            if v is None:
                continue
            format_columns += "{0}:={1}".format(k, k)
        sql = "update user_info set {} where user_id=:user_id".format(
            format_columns, **args)
        self.db_handle.query(sql)

    def get_head_val(self, user_id):
        key = "wwd_head_val_{}".format(user_id)
        head_val = self.redis_handle.get(key)
        if head_val:
            return common.my_str(head_val)
        sql = """
        select head_val from user_info where user_id=:user_id
        """
        result = self.db_handle.query(sql, user_id=user_id)
        return result[0].head_val if result.first() else ''

    def update_user_val(self, user_id, head_val):
        key = "wwd_head_val_{}".format(user_id)
        self.redis_handle.set(key, head_val, ex=7 * 60 * 60)
        sql = """
        update user_info set head_val=:head_val where user_id=:user_id
        """
        self.db_handle.query(sql, head_val=head_val, user_id=user_id)

    def upload_head_url(self, user_id, imgdata):
        """头像上传保存本地，并上传七牛"""
        rootpath = config.USERIMG_ROOT_PATH or os.path.dirname(__file__)
        # 分10个文件夹存储
        seq = user_id % 10 + 10000
        imgpath = os.path.abspath(os.path.join(rootpath, "head_url", str(seq)))
        if not os.path.exists(imgpath):
            os.makedirs(imgpath)
            os.chmod(imgpath, stat.S_IRWXG)
        strio = BytesIO(imgdata)
        img = Image.open(strio)
        filename = "wwd_head_{0}.jpg".format(user_id)
        path = os.path.join(imgpath, filename)
        try:
            img.save(path, quality=100)
        except:
            img = img.convert('RGB')
            img.save(path, quality=100)
        sizes = (160, 80)
        head_val = "ww{0}".format(int(time.time()))
        hash_value, key_value = "", ""
        for size in sizes:
            imgname = "wwd_head_{0}_{1}.jpg".format(user_id, size)
            path = os.path.join(imgpath, imgname)
            thum_size = (size, size)
            thum = img.resize(thum_size, Image.BILINEAR)
            thum.save(path, quality=100)
            bucket_name = "head-img"
            upload_key = "head_url/{seq}/wwd_head_{user_id}_{size}_{head_val}.jpg".format(
                user_id=user_id, size=size, head_val=head_val, seq=seq)
            hash_value, key_value = qiniu_tools.upload_file(
                bucket_name, upload_key, path)
        if all([hash_value, key_value]):
            self.update_user_val(user_id, head_val)
            return True
        else:
            send_try_except()
            return False

    def unbind_user_opendid_info(self, user_id):
        """账号注销，清除微信等绑定信息"""
        sql = """
        delete from openid_info where user_id=:user_id
        """
        self.db_handle.query(sql, user_id=user_id)


if __name__ == '__main__':
    import json

    handle = Handle()
    user_info = handle.get_user_info(237054765)
    print(json.dumps(user_info, ensure_ascii=False, indent=4))
