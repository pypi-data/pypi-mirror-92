import functools

import msgpack
import msgpack_numpy
from redis import Redis, from_url


@functools.lru_cache(maxsize=8)
def _Redis(**kwargs):
    if 'url' in kwargs:
        url = kwargs.pop('url')
        return from_url(url, **kwargs)
    return Redis(**kwargs)


def to_redis(obj):
    if isinstance(obj, str):
        obj = _Redis(url=obj)
    elif isinstance(obj, dict):
        obj = _Redis(**obj)
    return obj


def pack(data):
    return msgpack.packb(data, use_bin_type=True, default=msgpack_numpy.encode)


def unpack(buff):
    return msgpack.unpackb(buff, raw=False, object_hook=msgpack_numpy.decode)
