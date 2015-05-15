# -*- coding: utf-8 *-
import requests
from .decorators import cachable


class CachableRequests(object):
    @cachable
    def get(self, *args, **kwds):
        return requests.get(*args, **kwds)

    @cachable
    def post(self, *args, **kwds):
        return requests.post(*args, **kwds)

core = CachableRequests()
get = core.get
post = core.post
