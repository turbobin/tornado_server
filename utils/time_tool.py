# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta, timezone
import calendar
from dateutil.relativedelta import relativedelta


def utcnow():
    """
    获取utc时间
    """
    return int(datetime.now(timezone.utc).timestamp())


def utc_dt():
    return datetime.now(timezone.utc)


def today_is_friday():
    today_dt = datetime.now(timezone.utc).date()
    return today_dt.weekday() == 4


def get_ts_by_dayid(day_id):
    day_dt = datetime.strptime(str(day_id), '%Y%m%d')
    date = int(day_dt.replace(tzinfo=timezone.utc).timestamp())
    return date


def get_dayid_by_ts(ts):
    dt = get_date_by_ts(ts)
    date = get_dayid_by_dt(dt)
    return date


def get_dayid_by_dt(dt):
    try:
        day_id = int(dt.strftime('%Y%m%d'))
    except:
        day_id = 0
    return day_id


def get_date_by_ts(ts):
    return datetime.fromtimestamp(ts, timezone.utc)


def get_day(delta=0):
    today_dt = datetime.utcnow().date()
    day_dt = today_dt + timedelta(delta)
    day_id = int(day_dt.strftime('%Y%m%d'))
    return day_id


def get_yearmonthday(day_id):
    str_day_id = str(day_id)
    year = str_day_id[:4]
    month = str_day_id[4:6]
    day = str_day_id[-2:]
    return year, month, day


def someday_zero(delay=0):
    """
    @delay: timestamp of zero clock after `delay` days
    @return: timestamp
    """
    t = time.localtime(time.time())
    today = time.mktime(
        time.strptime(
            time.strftime("%Y-%m-%d 00:00:00", t), "%Y-%m-%d %H:%M:%S"))
    second_one_day = 24 * 60 * 60
    return int(today + delay * second_one_day)


def get_delta_ts(base_dt, months=0, weeks=0, days=0):
    delta_dt = base_dt + relativedelta(months=months, weeks=weeks, days=days)
    return int(delta_dt.timestamp())


def is_ts_offset_error(ts_offset):
    return ts_offset < -12 * 3600 or ts_offset > 14 * 3600


def is_utc_ts_error(ts):
    return (utcnow() - ts) > 60


def get_this_week_dayids(user_dt):
    dayids = []
    sunday_dt = user_dt + timedelta(-user_dt.weekday() - 1)
    for delta in range(7):
        day_dt = sunday_dt + timedelta(delta)
        day_id = get_dayid_by_dt(day_dt)
        dayids.append(day_id)
    return dayids


def get_one_week_befor_dayids_iso(user_dt, days_befor=0):
    dayids = []
    sunday_dt = user_dt + timedelta(-user_dt.weekday() + days_befor)
    for delta in range(-7, 0):
        day_dt = sunday_dt + timedelta(delta)
        day_id = get_dayid_by_dt(day_dt)
        dayids.append(day_id)
    return dayids


def get_two_week_befor_dayids_iso(user_dt, days_befor=0):
    dayids = []
    sunday_dt = user_dt + timedelta(-user_dt.weekday() + days_befor)
    for delta in range(-14, -7):
        day_dt = sunday_dt + timedelta(delta)
        day_id = get_dayid_by_dt(day_dt)
        dayids.append(day_id)
    return dayids


def get_three_week_befor_dayids_iso(user_dt, days_befor=0):
    dayids = []
    sunday_dt = user_dt + timedelta(-user_dt.weekday() + days_befor)
    for delta in range(-21, -14):
        day_dt = sunday_dt + timedelta(delta)
        day_id = get_dayid_by_dt(day_dt)
        dayids.append(day_id)
    return dayids


def get_isocalendar():
    return datetime.utcnow().isocalendar()


def get_month_day_range(delta=0):
    today = datetime.utcnow()
    yestoday = today + timedelta(delta)
    __, day_end = calendar.monthrange(yestoday.year, yestoday.month)
    return yestoday.year, yestoday.month, day_end


def get_months_befor_day_range(month=0):
    first = datetime(datetime.today().year, datetime.today().month - month, 1)
    last = datetime(datetime.today().year, datetime.today().month - month + 1, 1) - timedelta(1)
    return get_dayid_by_dt(first), get_dayid_by_dt(last)


if __name__ == '__main__':
    print (utcnow())
    print(datetime.now().timestamp())
    print(time.time())
    print(get_date_by_ts(28800 + 1564020151))
    today_dt = utc_dt()
    f, l = get_months_befor_day_range(1)
    print(f, l)
