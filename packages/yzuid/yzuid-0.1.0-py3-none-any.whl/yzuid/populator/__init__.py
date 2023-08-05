#!/usr/bin/python3.6.8+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-12-2
@desc: ...
"""
import abc
from enum import Enum

from ..utils import time_util
from ..id import Id, IdMeta


class PopulatorType(str, Enum):
    SYNC = 'sync'
    LOCK = 'lock'
    ATOMIC = 'atomic'


class PopulatorBase(metaclass=abc.ABCMeta):
    last_timestamp = -1
    sequence = 0

    # @property
    # def sequence(self):
    #     pass

    @abc.abstractmethod
    def populate_id(self, id_ins: Id, id_meta: IdMeta):
        """
        查看当前时间是否已经到了下一个时间单位了，
        如果到了，则将序号清零。
        如果还在上一个时间单位，就对序列号进行累加。
        如果累加后越界了，就需要等待下一时间单位再产生唯一ID

        :param id_ins:
        :param id_meta:
        :return:
        """
        timestamp = time_util.generate_time(id_ins.get_type())
        time_util.validate_timestamp(self.last_timestamp, timestamp)
        if timestamp == self.last_timestamp:
            self.sequence += 1
            self.sequence &= id_meta.get_sequence_bits_mask()
            if self.sequence == 0:
                timestamp = time_util.till_next_time(
                    self.last_timestamp, id_ins.get_type())
        else:
            self.last_timestamp = timestamp
            self.sequence = 0

        id_ins.set_sequence(self.sequence)
        id_ins.set_time(self.last_timestamp)

    @classmethod
    def reset(cls):
        cls.sequence = 0
        cls.last_timestamp = -1


from .atomic_populator import AtomicPopulator
from .lock_populator import LockPopulator
from .sync_populator import SyncPopulator
