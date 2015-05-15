# -*- coding: utf-8 -*-
from .caches import CachableRequestContext


def cachable(func):
    def _wrap(self, *args, **kwds):
        context = CachableRequestContext(*args, **kwds)
        res = context.load()
        if res:
            return res
        res = func(self, *args, **kwds)
        context.save(res)
        return res
    return _wrap
