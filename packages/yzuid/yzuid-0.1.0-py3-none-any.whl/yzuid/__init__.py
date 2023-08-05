#!/usr/bin/python3.6.8+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-12-2
@desc: ...
"""
from yzuid.id import IdService


def get_uid_service(
        machine_id: int = 1,
        gen_method: int = 2,
        m_type: int = 1,
        version: int = 0
):
    """

    :param machine_id:
    :param gen_method:
    :param m_type:
    :param version:
    :return:
    """
    return IdService(machine_id, gen_method, m_type, version)


