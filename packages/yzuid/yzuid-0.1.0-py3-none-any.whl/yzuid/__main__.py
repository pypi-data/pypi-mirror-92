#!/usr/bin/python3.6.8+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-12-2
@desc: ...
"""
import sys
import time
from yzuid import get_uid_service


if __name__ == '__main__':
    # sys.argv

    import time
    idsvc = get_uid_service(m_type=0)
    for _ in range(3):
        time.sleep(0.3)
        _id = idsvc.generate_id()
        print("===>generate_id: ", _id)
        id_obj = idsvc.explain_id(_id)
        print("===>explain_id: ", id_obj.__dict__)

        timestamp = idsvc.translate_time(id_obj.get_time())
        print("===>timestamp: ", timestamp)

        makeid = idsvc.make_id(
            sequence=id_obj.get_sequence(),
            timestamp=timestamp,
            machine=id_obj.get_machine(),
            method=id_obj.get_method(),
            mtype=id_obj.get_type(),
            version=id_obj.get_version()
        )
        print("===>make_id: ", makeid)
        id_obj = idsvc.explain_id(makeid)
        print("===>explain_id: ", id_obj.__dict__)



