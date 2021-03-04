#!/usr/bin/python
# -*- coding: UTF-8 -*-

from datetime import timedelta, datetime
import calendar


def is_month_range(tax_start, tax_end):
    if tax_start.day != 1:
        return False
    if tax_start.month != tax_end.month or tax_start.year != tax_end.year:
        return False
    month_end = (tax_start + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    return month_end.day == tax_end.day


def is_quarter_range(tax_start, tax_end):
    if tax_start.day != 1:
        return False
    if tax_start.month not in [1, 4, 7, 10]:
        return False
    if tax_start.month + 2 != tax_end.month or tax_start.year != tax_end.year:
        return False
    quarter_end = (tax_start + timedelta(days=93)).replace(day=1) - timedelta(days=1)
    return quarter_end.day == tax_end.day


def is_half_year_range(tax_start, tax_end):
    if tax_start.day != 1:
        return False
    if tax_start.year != tax_end.year:
        return False
    if tax_start.month == 1:
        return tax_end.month == 6 and tax_end.day == 30
    elif tax_start.month == 7:
        return tax_end.month == 12 and tax_end.day == 31
    return False


def is_year_range(tax_start, tax_end):
    return all([
        tax_start.year == tax_end.year,
        tax_start.month == 1,
        tax_start.day == 1,
        tax_end.month == 12,
        tax_end.day == 31
    ])


def ensure_datetime(o, format="%Y-%m-%d %H:%M:%S"):
    if isinstance(o, str):
        return datetime.strptime(o, format)
    elif isinstance(o, datetime):
        return o
    else:
        return o

def datetime_toString(dt, format="%Y-%m-%d"):
    return dt.strftime(format)

def get_month_date(today):
    today = ensure_datetime(today)
    year = today.year
    month = today.month
    start_day = 1
    if today.month == 1:
        year = today.year - 1
        month = 12
        _, last_day = calendar.monthrange(today.year - 1, month)
    else:
        _, last_day = calendar.monthrange(year, month)
    return datetime(year, month, start_day), datetime(year, month, last_day)


def get_month_bf_date(today=datetime.today()):
    """
    获取当前月份前一月
    args today 当前时间
    :return 202101
    """
    today = ensure_datetime(today)
    year = today.year
    month = today.month
    start_day = 1
    if today.month == 1:
        year = today.year - 1
        month = 12
        _, last_day = calendar.monthrange(today.year - 1, month)
    else:
        _, last_day = calendar.monthrange(year, month)
    # return ''.join([str(year), str(month)])
    return datetime(year, month, start_day).strftime("%Y%m")  # 202102


def get_lastseason_date(today):
    today = ensure_datetime(today)
    quarter = int((today.month - 1) / 3 + 1)
    year = today.year
    start_day = 1
    stop_day = 31
    if quarter == 1:
        year = year - 1
        month = 12
    elif quarter == 2:
        year = today.year
        month = 3
    elif quarter == 3:
        month = 6
        stop_day = 30
    else:
        month = 9
        stop_day = 30

    return datetime(year, month - 2, start_day), datetime(year, month, stop_day)


def get_year_date(today):
    today = ensure_datetime(today)
    return datetime(today.year - 1, 1, 1), datetime(today.year - 1, 12, 31)


def get_half_year_date(today):
    today = ensure_datetime(today)
    if today.month <= 5:
        return datetime(today.year - 1, 6, 1), datetime(today.year - 1, 12, 31)
    else:
        return datetime(today.year, 1, 1), datetime(today.year, 5, 31)


def get_declaration_period(frequency, today):
    if frequency == "year" or frequency == '年' or frequency == '年度':
        return get_year_date(today)
    if frequency == "quarter" or frequency == '季' or frequency == '季度':
        return get_lastseason_date(today)
    if frequency == "month" or frequency == '月' or frequency == '月度':
        return get_month_date(today)
    if frequency == "count" or frequency == '次':
        return get_month_date(today)
    if frequency == "half_year" or frequency == '半年':
        return get_half_year_date(today)


def datetime_toString(dt, format="%Y-%m-%d"):
    return dt.strftime(format)


# def string_toDatetime(string, format="%Y-%m-%d"):
def string_toDatetime(string, format="%Y/%m/%d"):
    return datetime.strptime(string, format)


if __name__ == '__main__':
    today = datetime.today()
    x, y = get_month_date(today)

    print(get_month_date(today))
    print(datetime_toString(x))
    print(datetime_toString(y))

    # frequency = 'count'
    # today = datetime.today()
    # start_, stop_ = get_declaration_period(frequency, today)
    # print(is_month_range(start_, stop_))
    # aa = "														2021/01/08"
    # print(aa.strip())
    # bb = string_toDatetime(aa.strip())
    # print(bb)
    # print(bb.month)
