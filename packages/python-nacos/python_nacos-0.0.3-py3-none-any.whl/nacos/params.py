# -*- coding: utf-8 -*-
from .exception import NacosException

VALID_CHAR = {'_', '-', '.', ':'}
PARAM_KEYS = ["data_id", "group"]
DEFAULT_GROUP_NAME = "DEFAULT_GROUP"


def is_valid(param):
    if not param:
        return False
    for i in param:
        if i.isalpha() or i.isdigit() or i in VALID_CHAR:
            continue
        return False
    return True


def check_params(params):
    for p in PARAM_KEYS:
        if p in params and not is_valid(params[p]):
            return False
    return True


def group_key(data_id, group, namespace):
    return "+".join([data_id, group, namespace])


def parse_key(key):
    sp = key.split("+")
    return sp[0], sp[1], sp[2]


def process_common_config_params(data_id, group):
    if not group or not group.strip():
        group = DEFAULT_GROUP_NAME
    else:
        group = group.strip()

    if not data_id or not is_valid(data_id):
        raise NacosException("Invalid dataId.")

    if not is_valid(group):
        raise NacosException("Invalid group.")
    return data_id, group
