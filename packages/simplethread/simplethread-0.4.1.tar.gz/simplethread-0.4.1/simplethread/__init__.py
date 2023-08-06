# -*- coding: utf-8 -*-

"""
Some useful utilities for Python's ``threading`` module.
"""

from typing import List

from simplethread.decorators import synchronized
from simplethread.decorators import threaded

__all__: List[str] = ["synchronized", "threaded"]
