# -*- coding: utf-8 -*-
import six
if six.PY3:
    import enum
else:
    import enum34 as enum  # noqa


class UserAgent(enum.Enum):
    FIREFOX = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:9.0.1) Gecko/20100101 Firefox/9.0.1)'  # 9.0
