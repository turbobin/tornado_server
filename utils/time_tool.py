# -*- coding: utf-8 -*-
import time
import arrow    # 需要先 pip install arrow
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta    # 需要先pip install python-dateutil


def get_day_id(delta=0):
    """获取某天的day_id"""
    date = datetime.now() + timedelta(days=delta)
    day_id = int(date.strftime('%Y%m%d'))
    return day_id


def get_day_id_by_ts(ts, delta=0):
    """根据获取时间戳day_id"""
    dt = datetime.fromtimestamp(ts) + timedelta(days=delta)
    day_id = int(dt.strftime('%Y%m%d'))
    return day_id


def get_ts_by_day_id(day_id, delta=0, hour=0, minute=0, second=0):
    """获取某一天(时 分 秒)的时间戳"""
    dt_format = "%d %d:%d:%d" %(day_id, hour, minute, second)
    st = time.strptime(dt_format, "%Y%m%d %H:%M:%S")
    ts = time.mktime(st) + 86400 * delta
    return int(ts)


def get_day_id_by_date(date, delta=0):
    """根据date获取day_id"""
    dt = date + timedelta(days=delta)
    day_id = int(dt.strftime('%Y%m%d'))
    return day_id


def get_date_by_day_id(day_id, delta=0, hour=0, minute=0, second=0):
    """获取某一天(时 分 秒)的date"""
    dt_format = "%d %d:%d:%d" %(day_id, hour, minute, second)
    st = time.strptime(dt_format, "%Y%m%d %H:%M:%S")
    ts = time.mktime(st) + 86400 * delta
    return datetime.fromtimestamp(ts)


def get_week_id(delta=0):
    """今年的第几周"""
    date = datetime.now() + timedelta(weeks=delta)
    year, week_id, __ = date.isocalendar()
    return year, week_id


def get_week_start_day_id(delta=0):
    """一周的开始日期"""
    date = datetime.now() + timedelta(weeks=delta)
    week_begin = (date - timedelta(days=date.weekday())).strftime('%Y%m%d')
    return int(week_begin)


def get_week_end_day_id(delta=0):
    """一周结束日期"""
    date = datetime.now() + timedelta(weeks=delta)
    week_end = (date + timedelta(days=6-date.weekday())).strftime('%Y%m%d')
    return int(week_end)


def get_month_start_day_id(delta=0):
    """月开始日期"""
    now = datetime.now()
    month_start = datetime(now.year, now.month + delta, 1).strftime('%Y%m%d')
    return int(month_start)


def get_month_end_day_id(delta=0):
    """月结束日期"""
    now = datetime.now()
    month_end_date = datetime(now.year, now.month + 1 + delta, 1) - timedelta(days=1)
    return int(month_end_date.strftime('%Y%m%d'))


def get_relative_date(date, delta=0, relative_type="day"):
    """获取相对日期"""
    relative_date = date
    if relative_type == "hour":
        relative_date = date + relativedelta(hours=delta)
    elif relative_type == "day":
        relative_date = date + relativedelta(days=delta)
    elif relative_type == "week":
        relative_date = date + relativedelta(weeks=delta)
    elif relative_type == "month":
        relative_date = date + relativedelta(months=delta)
    elif relative_type == "year":
        relative_date = date + relativedelta(years=delta)
    return relative_date


def get_humanize_time(date, lg="zh"):
    """返回可读化时间"""
    a = arrow.get(date, tzinfo='local')
    return a.humanize(locale=lg)


def date_format(date, f="YYYY-MM-DD HH:mm:ss"):
    """日期格式化，可以传date对象或时间戳"""
    return arrow.get(date, tzinfo='local').format(f)


if __name__ == '__main__':
    print('1：', get_day_id(0))
    print('2：', get_day_id_by_ts(1563811200, 0))
    print('3：', get_ts_by_day_id(20200312, -1))
    print('4：', get_week_id())
    print('5：', get_week_start_day_id(0))
    print('6：', get_week_end_day_id(0))
    print('7：', get_month_start_day_id(0))
    print('8：', get_month_end_day_id(-3))
    print('9：', get_relative_date(datetime.now(), 1, "month"))
    print('10：', get_humanize_time(time.time() - 60, "zh"))
    print('11：', date_format(time.time()))
