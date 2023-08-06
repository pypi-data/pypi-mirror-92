# -*- coding: utf-8 -*-

import logging
import os.path

try:
    import fcntl

    use_fcntl = True
except (Exception,):
    use_fcntl = False

logger = logging.getLogger("nacos")


def read_file_str(base, key):
    content = read_file(base, key)
    return content.decode("UTF-8") if isinstance(content, bytes) else content


def read_file(base, key):
    file_path = os.path.join(base, key)
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "r+", encoding="UTF-8", newline="") as f:
            lock_file(f)
            return f.read()
    except OSError:
        logger.exception("[read-file] read file failed, file path:%s" % file_path)
        return None


def save_file(base, key, content):
    file_path = os.path.join(base, key)
    if not os.path.isdir(base):
        os.makedirs(base, exist_ok=True)
    try:
        with open(file_path, "wb") as f:
            lock_file(f)
            f.write(content if isinstance(content, bytes) else content.encode("UTF-8"))
    except OSError:
        logger.exception("[save-file] save file failed, file path:%s" % file_path)


def delete_file(base, key):
    file_path = os.path.join(base, key)
    try:
        os.remove(file_path)
    except OSError:
        logger.warning("[delete-file] file not exists, file path:%s" % file_path)


def lock_file(f):
    if use_fcntl:
        fcntl.flock(f, fcntl.LOCK_EX)
