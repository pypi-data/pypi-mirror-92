#!/usr/bin/python3.6.8+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-12-2
@desc: ...
"""
from . import PopulatorBase


class SyncPopulator(PopulatorBase):
    """"""
    def populate_id(self, id_ins, id_meta):
        super().populate_id(id_ins, id_meta)
