#!/usr/bin/python3.6.8+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-12-2
@desc: ...
"""
import time
from typing import Union
from ..id import IdType

EPOCH = 1610351662000


def timestamp2duration(timestamp: int, level='s') -> int:
    """
    将时间戳转为时间间隔数值
    :param timestamp:
    :return:
    """
    if level == 's':
        timestamp = timestamp*1000

    value = timestamp - EPOCH
    if value < 0:
        raise ValueError('时间戳超出计算范围')
    result = value if level == 'ms' else value/1000
    return int(result)


def duration2timestamp(duration: int, level='s') -> int:
    """"""
    if level not in ['s', 'ms']:
        ValueError(f'Error: <level:{level}> not in ["s", "ms"]')

    if level == 's':
        duration = duration * 1000
    timestamp = duration + EPOCH
    if level == 's':
        timestamp = timestamp/1000
    return int(timestamp)


def generate_time(idtype: int):
    if idtype == IdType.MAX_PEAK.value:
        return int(time.time() - (EPOCH/1000))
    elif idtype == IdType.MIN_GRANULARITY.value:
        return int(time.time()*1000 - EPOCH)
    else:
        return int(time.time() - (EPOCH / 1000))


def validate_timestamp(last_timestamp, timestamp):
    if timestamp < last_timestamp:
        raise ValueError(
            "Clock moved backwards.  "
            "Refusing to generate id for %d second/milisecond.",
            (last_timestamp-timestamp)
        )


def till_next_time(last_timestamp, idtype):
    timestamp = generate_time(idtype)
    while timestamp <= last_timestamp:
        timestamp = generate_time(idtype)
