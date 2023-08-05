#!/usr/bin/python3.6.8+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-12-2
@desc: ...
"""


class Id:
    """
    __machine: 机器序号
    __sequence: 在时间单位内的序号
    __time: 项目启动到现在的秒数
    __method: (嵌入式，restful，中心分发）
    __type: （最大峰值，最小粒度）
    __version:
    """

    __machine = None
    __sequence = None
    __time = None
    __method = None
    __type = None
    __version = None

    def get_sequence(self) -> int:
        return self.__sequence

    def set_sequence(self, sequence):
        self.__sequence = sequence

    def get_time(self) -> int:
        return self.__time

    def set_time(self, seconds: int):
        self.__time = seconds

    def get_machine(self) -> int:
        return self.__machine

    def set_machine(self, machine_id: int):
        self.__machine = machine_id

    def get_method(self) -> int:
        return self.__method

    def set_method(self, method: int):
        if method not in [0, 1, 2, 3]:
            raise ValueError('Error: method not in [0, 1, 2, 3]')
        self.__method = method

    def get_type(self) -> int:
        return self.__type

    def set_type(self, typ: int):
        if typ not in [0, 1]:
            raise ValueError('Error: typ not in [0, 1]')
        self.__type = typ

    def get_version(self) -> int:
        return self.__version

    def set_version(self, version: int):
        if version not in [0, 1]:
            raise ValueError('Error: version not in [0, 1]')
        self.__version = version

    def _validate_range(self, typ, bits):
        """
        验证值范围

        :param typ:
        :param bits:
        :return:
        """


