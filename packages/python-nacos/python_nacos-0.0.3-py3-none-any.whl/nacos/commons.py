# -*- coding: utf-8 -*-
import json


def synchronized_with_attr(attr_name):
    def decorator(func):
        def synced_func(*args, **kws):
            self = args[0]
            lock = getattr(self, attr_name)
            with lock:
                return func(*args, **kws)

        return synced_func

    return decorator


def truncate(ori_str, length=100):
    if not ori_str:
        return ""
    if not isinstance(ori_str, str):
        ori_str = json.dumps(ori_str)
    return ori_str[:length] + "..." if len(ori_str) > length else ori_str
