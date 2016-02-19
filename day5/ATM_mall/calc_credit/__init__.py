#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""

def get_diff_days(start_time, end_time):
    """
    :param start_time: 开始日期
    :param end_time: 结束日期
    :return: 相差天数
    """
    import datetime
    import re
    date_format = "%Y-%m-%d"
    start_time = re.sub("[/]+", "-", str(start_time))
    end_time = re.sub("[/]+", "-", str(end_time))
    try:
        start_time = datetime.datetime.strptime(str(start_time), date_format)
        end_time = datetime.datetime.strptime(str(end_time), date_format)
        differ = end_time - start_time
        days = differ.days
    except ValueError:
        return False
    return str(days)


def get_new_balance(last_balance, payment, new_charges, adjustment, interest):
    """
    :param last_balance: 上期账单金额
    :param payment: 上期还款金额
    :param new_charges: 本期账单金额
    :param adjustment: 本期调整金额
    :param interest: 循环利息
    :return: 本期还款总额
    """
    balance = last_balance - payment + new_charges - adjustment + interest
    return balance


def withdraw_money(money, commission, days, flag=False):
    """
    :param money: 取现金额
    :param commission: 手续费率
    :param days: 还款天数
    :param flag: 是否已计算手续费
    :return: 最终还款金额
    """
    if days > 30:  # 大于30天开始滚利
        if not flag:
            total_interest = money * commission + money * 0.0005 * 30  # 计算30天利息
            flag = True
        else:
            total_interest = money * 0.0005 * 30
        reduce_days = days - 30  # 减去30天算剩余天数
        new_balance = total_interest + money  # 滚利,本息相加
        return withdraw_money(new_balance, 0.05, reduce_days, flag=flag)
    if flag:
        total_interest = money + money * 0.0005 * days
    else:
        total_interest = money * commission + money + money * 0.0005 * days  # 计算本息
    return total_interest
