#!/usr/bin/python3.6.8+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2021-1-11
@desc: ...

ID类型分为最大峰值和最小粒度
【最大峰值】：
| 版本 | 类型 | 生成方式 | 秒级时间 | 序列号 | 机器ID |
| 63   | 62  | 60-61  | 59-30   | 29-10 | 0-9   |

【最小粒度】：
| 版本 | 类型 | 生成方式 | 秒级时间 | 序列号 | 机器ID |
| 63   | 62  | 60-61  | 59-20   | 19-10 | 0-9   |


"""
import time
from yzuid.id import get_idmeta
from yzuid.populator import *
from yzuid.converter import IdConvert
from yzuid.id import Id, IdType
from yzuid.utils import time_util


class IdServiceBase(metaclass=abc.ABCMeta):
    """
    ID生成器的接口抽象基类
    """
    @abc.abstractmethod
    def generate_id(self):
        pass

    @abc.abstractmethod
    def explain_id(self, id_int: int):
        pass

    @abc.abstractmethod
    def make_id(
            self, sequence: int, time_stamp: int,
            machine: int=None, method: int=None,
            mtype: int=None, version: int=None
    ):
        pass

    @abc.abstractmethod
    def translate_time(self, time_duration: int, typ: int):
        """"""


class IdService(IdServiceBase):
    def __init__(
            self,
            machine: int,
            method: int,
            mtype: int,
            version: int,
            populator_type: PopulatorType = "sync"
    ):
        self.machine = machine
        self.method = method
        self.mtype = mtype
        self.version = version
        self._idmeta = self._init_meta()
        self._populator = self._init_populator(populator_type)
        self._converter = self._init_converter()

    def _init_meta(self):
        return get_idmeta(self.mtype)

    def _init_populator(self, populator_type: str):
        if populator_type == PopulatorType.SYNC.value:
            return SyncPopulator()
        elif populator_type == PopulatorType.LOCK.value:
            return LockPopulator()
        elif populator_type == PopulatorType.ATOMIC.value:
            return AtomicPopulator()
        else:
            raise

    def _init_converter(self):
        return IdConvert(self._idmeta)

    def generate_id(self) -> int:
        """生成长整型ID"""
        id_obj = Id()
        id_obj.set_machine(self.machine)
        id_obj.set_method(self.method)
        id_obj.set_type(self.mtype)
        id_obj.set_version(self.version)

        self._populator.populate_id(id_obj, self._idmeta)
        ret = self._converter.convert_to_generate(id_obj)
        return ret

    def explain_id(self, id_int: int) -> Id:
        """解析长整型ID为Id的实例"""
        return self._converter.convert_to_explain(id_int)

    def make_id(
            self, sequence: int, timestamp: int,
            machine: int=None, method: int=None,
            mtype: int=None, version: int=None
    ) -> int:
        """
        手动合成ID，慎用！
        限制手动合成的ID只能为过去的时间，防止未来时间的ID重复
        :param sequence:
        :param timestamp:
        :param machine:
        :param method:
        :param mtype:
        :param version:
        :return:
        """
        if not isinstance(timestamp, int):
            raise ValueError("The param of <time: int> need int classtype.")
        if mtype is None:
            mtype = self.mtype
        if mtype == IdType.MIN_GRANULARITY.value:
            if len(str(timestamp)) != 13 or (int(time.time()*1000) - timestamp):
                ValueError(f"Error: <time_stamp:{timestamp}> is error.")
            time_duration = time_util.timestamp2duration(timestamp, level='ms')
        else:
            if len(str(timestamp)) != 10 or (int(time.time()) - timestamp):
                ValueError(f"Error: <time_stamp:{timestamp}> is error.")
            time_duration = time_util.timestamp2duration(timestamp)

        # 实例化Id对象
        _id = Id()
        _id.set_sequence(sequence)
        _id.set_time(time_duration)
        _id.set_method(method or self.method)
        _id.set_type(mtype or self.mtype)
        _id.set_version(version or self.version)
        _id.set_machine(machine or self.machine)
        ret = self._converter.convert_to_generate(_id)
        return ret

    def translate_time(self, time_duration: int, typ: int=None):
        """
        从时间间隔中计算出时间戳
        :param time_duration:
        :param typ:
        :return:
        """
        if typ is None:
            typ = self.mtype
        level = 's' if typ == IdType.MAX_PEAK.value else 'ms'
        return time_util.duration2timestamp(time_duration, level)

    def _validate_range(self, typ, bits):
        """
        验证值范围

        :param typ:
        :param bits:
        :return:
        """

