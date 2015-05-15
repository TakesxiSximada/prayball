# -*- coding: utf-8 -*-


class XPathContext(object):
    def __init__(self, core):
        self._core = core

    def xpath(self, *args, **kwds):
        return self._core.xpath(*args, **kwds)
