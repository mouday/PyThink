# -*- coding: utf-8 -*-

# @Date    : 2019-04-30
# @Author  : Peng Shiyu


from collections import namedtuple


class Records(object):
    """数据 select 之后的结果集 """

    def __init__(self, keys, rows, rowcount):
        self._keys = keys
        self._rows = rows
        self._rowcount = rowcount
        self._point = 0
        self._Record = namedtuple("Record", keys)

    @property
    def rowcount(self):
        return self._rowcount

    def all(self, as_dict=False):
        """
        :param as_dict: bool 结果单元转为字典，默认为对象

        :return: list
        """

        if as_dict:
            lst = []
            for row in self._rows:
                items = zip(self._keys, row)
                lst.append(dict(items))
            return lst
        else:
            return [self._Record(*row) for row in self._rows]

    def first(self, as_dict=False):
        """
        :param as_dict: bool 结果转为字典，默认为对象
        :return: Record or dict
        """
        try:
            row = self._rows[0]
        except IndexError:
            return None

        if as_dict:
            items = zip(self._keys, row)
            return dict(items)
        else:
            return self._Record(*row)

    def __repr__(self):
        return '<Records size={}>'.format(self._rowcount)

    def __iter__(self):
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        if self._point < self._rowcount:
            row = self._rows[self._point]
            self._point += 1
            return self._Record(*row)
        else:
            raise StopIteration()
