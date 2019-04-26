# -*- coding: utf-8 -*-

# @Date    : 2019-04-26
# @Author  : Peng Shiyu

import hashlib
from datetime import datetime


class Util(object):
    """
    工具类
    """
    @classmethod
    def get_date_time_str(cls, datetime_format):
        return datetime.now().strftime(datetime_format)

    @classmethod
    def get_md5(cls, data, md5_list):
        md5 = hashlib.md5()

        for md5_field in md5_list:
            value = data[md5_field]

            md5.update("{}".format(value).encode("utf-8"))

        return md5.hexdigest()

    @classmethod
    def get_public_names(cls, obj):
        return filter(cls.is_public, dir(obj))

    @classmethod
    def is_public(cls, method_name):
        if all([
            not method_name.startswith("_"),
            not method_name.startswith("__")
        ]):
            return True
        else:
            return False

    @classmethod
    def get_method(cls, obj, method_name):
        method = getattr(obj, method_name)

        if callable(method):
            return method
        else:
            return None
