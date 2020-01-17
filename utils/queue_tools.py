# coding:utf8
"""
beanstalkc通用队列添加数据操作
"""
import sys

sys.path.append('..')
import json
import beanstalkc
import time
from configs import config

user_info_beanstalk = beanstalkc.Connection(
    host=config.BEANSTALK_ACTIVITY_HOST,
    port=config.BEANSTALK_ACTIVITY_PORT,
    parse_yaml=False,
    connect_timeout=None)


def put_beanstalk(data, task_name):
    """
    放到队列中
    """
    global user_info_beanstalk
    if not isinstance(data, dict):
        return
    msg = json.dumps(data, ensure_ascii=False)
    user_info_beanstalk.use(task_name)
    user_info_beanstalk.put(msg)


class Handle():
    @staticmethod
    def add_to_queue(user_id, task_name, data):
        """
        通用队列添加数据操作
        task_name -> str 唯一任务名称
        data -> dict
        """
        beanstalk_item = {}
        beanstalk_item['type'] = task_name
        beanstalk_item['worktype'] = task_name
        beanstalk_item['user_id'] = user_id
        beanstalk_item['data'] = data
        beanstalk_item['update_ts'] = int(time.time())
        put_beanstalk(beanstalk_item, task_name)


if __name__ == '__main__':
    task_name = "wwd_upload_head_url"
    data = dict(
        head_url=
        "https://head-img.51yund.com/head/474109/head_237054765_80.jpg?imageslim"
    )
    Handle().add_to_queue(255495082, task_name, data)
