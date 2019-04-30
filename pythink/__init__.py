# -*- coding: utf-8 -*-

# @Date    : 2019-04-13
# @Author  : Peng Shiyu

from __future__ import unicode_literals, print_function

from .think_database import ThinkDatabase
from .think_table import ThinkTable
from .think_model import ThinkModel
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

__version__ = open(os.path.join(base_dir, "VERSION")).read()

__all__ = [ThinkDatabase, ThinkTable, ThinkModel]
