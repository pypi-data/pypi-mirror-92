#!/usr/bin/python3.6.8+
# -*- coding:utf-8 -*-
from enum import Enum


class IdType(Enum):
    MAX_PEAK = 1            # 最大峰值
    MIN_GRANULARITY = 0     # 最小颗粒度


from ._id import Id
from ._id_meta import IdMeta, get_idmeta
from .id_service import IdService
