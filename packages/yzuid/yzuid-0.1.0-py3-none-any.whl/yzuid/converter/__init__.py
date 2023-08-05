#!/usr/bin/python3.6.8+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-12-2
@desc: ...
"""
import abc

from ..id import Id, IdMeta


class IdConvertBase(metaclass=abc.ABCMeta):
    """
    ID的长整型合成与拆解成实例的转换接口基类
    """
    @abc.abstractmethod
    def convert_to_generate(self, id_ins: Id) -> int:
        """把ID实例转换为一个长整型的ID"""
        pass

    @abc.abstractmethod
    def convert_to_explain(self, id_int: int) -> Id:
        """拆解长整型的ID"""
        pass


class IdConvert(IdConvertBase):
    """"""
    def __init__(self, id_meta: IdMeta):
        self.id_meta = id_meta

    def convert_to_generate(self, id_ins: Id) -> int:
        ret = 0
        ret |= id_ins.get_machine()
        ret |= id_ins.get_sequence() << self.id_meta.get_seq_bits_startpos()
        ret |= id_ins.get_time() << self.id_meta.get_time_bits_startpos()
        ret |= id_ins.get_method() << self.id_meta.get_method_bits_startpos()
        ret |= (id_ins.get_type() << self.id_meta.get_type_bits_startpos())
        ret |= id_ins.get_version() << self.id_meta.get_version_bits_startpos()
        return ret

    def convert_to_explain(self, id_int: int) -> Id:
        id_obj = Id()
        id_obj.set_machine(id_int & self.id_meta.get_machine_bits_mask())
        id_obj.set_sequence((id_int >> self.id_meta.get_seq_bits_startpos()) & self.id_meta.get_sequence_bits_mask())
        id_obj.set_time((id_int >> self.id_meta.get_time_bits_startpos()) & self.id_meta.get_time_bits_mask())
        id_obj.set_method((id_int >> self.id_meta.get_method_bits_startpos()) & self.id_meta.get_method_bits_mask())
        id_obj.set_type((id_int >> self.id_meta.get_type_bits_startpos()) & self.id_meta.get_type_bits_mask())
        id_obj.set_version((id_int >> self.id_meta.get_version_bits_startpos()) & self.id_meta.get_version_bits_mask())
        return id_obj
