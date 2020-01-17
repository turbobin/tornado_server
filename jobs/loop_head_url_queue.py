# coding:utf8
"""
消费队列信息
"""
import sys

import requests

sys.path.append('..')
import beanstalkc
import json
from configs import config
from utils import common
from utils.log import send_try_except
from handlers.user import user_handle


class Handle:
    def __init__(self, task_name):
        self.beanstalk = beanstalkc.Connection(
            host=config.BEANSTALK_ACTIVITY_HOST,
            port=config.BEANSTALK_ACTIVITY_PORT,
            parse_yaml=False,
            connect_timeout=None)
        self.beanstalk.use(task_name)
        self.beanstalk.watch(task_name)
        self.beanstalk.ignore("default")
        self.user_handle = user_handle.Handle()

    def run(self):
        """
        执行
        """
        job = self.beanstalk.reserve()
        data = json.loads(job.body)
        user_id = int(data['user_id'])
        if not user_id:
            return job.delete()
        if 'type' not in data.keys() or 'worktype' not in data.keys():
            return job.delete()
        raw_data = data['data']

        try:
            head_url = common.my_str(raw_data['head_url'])
            if head_url == "":
                return job.delete()

            imgdata = requests.get(head_url).content
            self.user_handle.upload_head_url(user_id, imgdata)
        except Exception:
            send_try_except()

        return job.delete()


if __name__ == '__main__':
    handle = Handle("wwd_upload_head_url")
    while 1:
        handle.run()
