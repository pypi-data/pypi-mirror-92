# -*- coding: utf-8 -*-
import hashlib
from urllib import parse


def url_encode(url):
    """url编码"""
    url_data = parse.quote(url)
    return url_data


def url_decode(url):
    """url解码"""
    url_data = parse.unquote(url)
    return url_data


def get_md5(content):
    """md5编码"""
    return hashlib.md5(content.encode("UTF-8")).hexdigest() if content is not None else None
