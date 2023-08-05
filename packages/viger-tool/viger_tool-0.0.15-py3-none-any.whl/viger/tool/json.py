#!/usr/bin/env python

"""
JSON 默認編碼改寫
"""

import json
from datetime import datetime
from json import JSONEncoder

class JSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        base_type = (str, int, float, dict, list)
        if (not isinstance(obj, base_type) and
                hasattr(obj, '__str__')):
            return str(obj)
        raise TypeError(f'Object of type {val.__class__.__name__} '
                                        f'is not JSON serializable')
# 調整默認值
def dumps(obj, *, skipkeys=False, ensure_ascii=False, check_circular=True,
        allow_nan=True, cls=None, indent=None, separators=None,
        default=None, sort_keys=False, **kw):

    if cls is None:
        cls = JSONEncoder
    return cls(
        skipkeys=skipkeys, ensure_ascii=ensure_ascii,
        check_circular=check_circular, allow_nan=allow_nan, indent=indent,
        separators=separators, default=default, sort_keys=sort_keys,
        **kw).encode(obj)

json.dumps = dumps
