# -*- coding: utf-8 -*-
import six
import os.path
import pickle
import hashlib

if six.PY3:
    import unittest.mock as mock
else:
    import mock  # noqa


class CachableRequestContext(object):
    def __init__(self, *args, **kwds):
        self.url = args[0] if args else 'url' in kwds and kwds.pop('pop', None)
        if not self.url:
            raise ValueError()

    @property
    def cache_path(self):
        url = self.url
        if type(url) is str:
            url = url.encode()
        return hashlib.md5(url).hexdigest()

    def load(self):
        if os.path.exists(self.cache_path):
            with open(self.cache_path, 'rb') as fp:
                return pickle.load(fp)

    def save(self, obj):
        with open(self.cache_path, 'w+b') as fp:
            pickle.dump(obj, fp)
