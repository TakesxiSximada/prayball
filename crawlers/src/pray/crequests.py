# -*- coding: utf-8 *-
import requests
from .decorators import cachable
from .useragents import UserAgent


class CachableRequests(object):
    def __init__(self, headers={}):
        self.headers = headers

    def process_headers(self, **kwds):
        headers = kwds.get('headers', {})
        headers.update(self.headers)
        kwds['headers'] = headers
        return kwds

    @cachable
    def get(self, *args, **kwds):
        kwds = self.process_headers(**kwds)
        return requests.get(*args, **kwds)

    @cachable
    def post(self, *args, **kwds):
        kwds = self.process_headers(**kwds)
        return requests.post(*args, **kwds)


DEFAULT_HEADERS = {
    'user-agent': UserAgent.FIREFOX,
    }

core = CachableRequests(headers=DEFAULT_HEADERS)
get = core.get
post = core.post
