# coding:utf8
"""
腾讯短信
"""

from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
from configs import config


def yd_send_sms_param(template_id, params, mobile, sms_sign):
    """
    指定模版发送
    """
    app_id = config.QCLOUD_SMS_APPID
    app_key = config.QCLOUD_SMS_APPKEY
    ssender = SmsSingleSender(app_id, app_key)
    try:
        result = ssender.send_with_param(86, mobile, template_id, params, sign=sms_sign)
    except HTTPError as e:
        print(e)
    except Exception as e:
        print(e)
