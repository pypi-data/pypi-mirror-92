#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2021 Liu Jianwei. All Rights Reserved.
# Author: Liu Jianwei
# Contact: tungliu@126.com
# Link: https://liujianwei.tech/

"""snowpaw.py"""

from __future__ import print_function
import logging
import time
from functools import wraps
from decimal import Decimal
from io import open

true = True
false = False
null = None
# with..as.. like java's try(...){}
# derivation/inheritance: Child(Super)
# this = self
Object = object
O = Object


def D(value):
    """if only string works here, why there are other constructor"""
    return Decimal(str(value))


def logaround(func):
    """log around"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info("function %s start", func.__name__)
        result = func(*args, **kwargs)
        logging.info("function %s end", func.__name__)
        return result

    return wrapper


def logelapsedtime(func):
    """logging elapsed time of function execution in milliseconds"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time() * 1000
        result = func(*args, **kwargs)
        elapsed = time.time() * 1000 - start
        logging.info("function: %s, elapsed time: %f ms", func.__name__, elapsed)
        return result

    return wrapper


def counter(n):
    """A general purpose counter, infinite loop in case n<=0"""
    n = n - 1
    while n != 0:
        yield n
        n = n - 1 if n > 0 else n
    yield n


def waits(interval=60, times=10):
    def decorator(func):
        """wait for func to be executed and returned as TRUE"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            for c in counter(times):
                if func(*args, **kwargs):
                    return true
                time.sleep(interval)
            return false

        return wrapper

    return decorator


def deprecated(func):
    """A soft-implementation to https://pypi.org/project/Python-Deprecated/"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper

if __name__ == '__main__':
    print('snowpaw is OK')
