#!/usr/bin/python3.6.8+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-12-2
@desc: ...
"""
from . import IdType


class IdMeta:
    def __init__(
            self,
            machine_bits: int,
            sequence_bits: int,
            time_bits: int,
            method_bits: int,
            type_bits: int,
            version_bits: int
    ):
        self.machine_bits = machine_bits
        self.sequence_bits = sequence_bits
        self.time_bits = time_bits
        self.method_bits = method_bits
        self.type_bits = type_bits
        self.version_bits = version_bits

    def get_machine_bits(self) -> int:
        return self.machine_bits

    def set_machine_bits(self, machine_bits: int):
        self.machine_bits = machine_bits

    def get_machine_bits_mask(self):
        return -1 ^ -1 << self.machine_bits
    
    def get_seq_bits_startpos(self):
        return self.machine_bits

    def get_sequence_bits(self) -> int:
        return self.sequence_bits

    def set_sequence_bits(self, sequence_bits: int):
        self.sequence_bits = sequence_bits

    def get_sequence_bits_mask(self):
        return -1 ^ -1 << self.sequence_bits

    def get_time_bits_startpos(self):
        return self.machine_bits + self.sequence_bits

    def get_time_bits(self) -> int:
        return self.time_bits

    def set_time_bits(self, time_bits: int):
        self.time_bits = time_bits

    def get_time_bits_mask(self):
        return -1 ^ -1 << self.time_bits

    def get_method_bits_startpos(self):
        return self.machine_bits + self.sequence_bits + self.time_bits
    
    def get_method_bits(self) -> int:
        return self.method_bits

    def set_method_bits(self, method_bits: int):
        self.method_bits = method_bits

    def get_method_bits_mask(self):
        return -1 ^ -1 << self.method_bits

    def get_type_bits_startpos(self):
        return self.get_method_bits_startpos() + self.method_bits
    
    def get_type_bits(self) -> int:
        return self.type_bits

    def set_type_bits(self, type_bits: int):
        self.type_bits = type_bits

    def get_type_bits_mask(self):
        return -1 ^ -1 << self.type_bits

    def get_version_bits_startpos(self):
        return self.get_type_bits_startpos() + self.type_bits
    
    def get_version_bits(self) -> int:
        return self.version_bits

    def set_version_bits(self, version_bits: int):
        self.version_bits = version_bits

    def get_version_bits_mask(self):
        return -1 ^ -1 << self.version_bits
    

def get_idmeta(idtype: int):
    if idtype == IdType.MAX_PEAK.value:
        return IdMeta(
            machine_bits=10,
            sequence_bits=20,
            time_bits=30,
            method_bits=2,
            type_bits=1,
            version_bits=1
        )
    elif idtype == IdType.MIN_GRANULARITY.value:
        return IdMeta(
            machine_bits=10,
            sequence_bits=10,
            time_bits=40,
            method_bits=2,
            type_bits=1,
            version_bits=1
        )
    else:
        raise
