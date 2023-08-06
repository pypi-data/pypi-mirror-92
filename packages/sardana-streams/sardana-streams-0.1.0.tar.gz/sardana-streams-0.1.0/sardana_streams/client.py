import datetime

import numpy

from .redis import to_redis, unpack


class Scan:

    def __init__(self, redis, key, meta):
        self.redis = redis
        self.key = key
        self.meta = meta
        self.rid = '.'.join(key.rsplit(':', 2)[-2:])
        dt = datetime.datetime.fromtimestamp(meta['start_ts'])
        self.meta['start_dt'] = dt
        size = meta['total_nb_points']
        dtypes = []
        ref_dtypes = []
        bitmap_dtypes = []
        for i, col in enumerate(meta['columns']):
            name = col['name']
            is_ref = col.get('value_ref_enabled', False)
            dtype = col['dtype'].replace('str', 'object')
            if col['shape'] and col['shape'][0] > 1:
                dtype = 'object'
            if is_ref:
                ref_dtypes.append((name, dtype))
                dtype = 'object'
            bitmap_dtypes.append((name, 'b'))
            dtypes.append((name, dtype))
        self._data = numpy.empty(size, dtype=dtypes)
        self._points = numpy.zeros(size, dtype=bitmap_dtypes)
        self.closed = False

    def __getattr__(self, name):
        return self.meta[name]

    def __getitem__(self, name):
        if isinstance(name, str):
            return self.data[name]
        else:
            data = self._data[name]
            return {f: data[f] for f in data.dtype.fields}

    def __len__(self):
        points = self._points
        size = min(points[f].argmin() for f in points.dtype.fields)
        if not size and all(points[0]):
            size = len(points)
        return size

    def set(self, point_nb, record):
        for name, value in record.items():
            self._set_point(point_nb, name, value)

    def _set_point(self, point_nb, name, value):
        if name not in self._data.dtype.fields:
            # ignore unknown fields for now
            return
        col = self._data[name]
        if col.dtype == 'object':
            v = col[point_nb]
            if v is None:
                v = {}
            key = 'ref' if isinstance(value, str) else 'value'
            v[key] = value
            value = v
        col[point_nb] = value
        self._points[name][point_nb] = True

    def close(self, tail=None):
        if tail is not None:
            self.meta.update(tail)
            dt = datetime.datetime.fromtimestamp(self.meta['end_ts'])
            self.meta['end_dt'] = dt
        self.closed = True

    @property
    def data(self):
        result = {}
        for field in self._data.dtype.fields:
            data, pts = self._data[field], self._points[field]
            n = pts.argmin()
            result[field] = data if not n and all(pts) else data[:n]
        return result


def handle(redis, scan, etype, key, data):
    data = unpack(data)
    if etype == 'header':
        data['redis'] = key
        scan = Scan(redis, key, data)
    elif etype == 'record':
        base_key, index = key.rsplit(':points:', 1)
        if scan is None:
            scan = load_scan_from_redis(redis, base_key)
        elif scan.key == base_key:
            point_nb = int(index.split(':', 1)[0])
            scan.set(point_nb, data)
        else:
            # ignore out of order scan (maybe a previous scan
            # delayed post-processing data)
            return
    elif etype == 'tail':
        scan.close(data)
    return scan, etype, key, data


class ScanStream:

    def __init__(self, redis, prefix):
        self.redis = to_redis(redis)
        self.prefix = prefix
        self._pubsub = None
        self.scan = None

    def __iter__(self):
        if self._pubsub is not None:
            raise RuntimeError('Stream already running')
        self.scan = None
        with self.redis.pubsub() as pubsub:
            self._pubsub = pubsub
            pubsub.subscribe(self.prefix)
            for event in pubsub.listen():
                msg_type = event['type']
                if msg_type == 'subscribe':
                    continue
                elif msg_type == 'unsubscribe':
                    break
                key, etype, data = event['data'].split(b'|', 2)
                key, etype = key.decode(), etype.decode()
                result = handle(self.redis, self.scan, etype, key, data)
                if result is None:  # (probably out of order delayed event)
                    continue
                self.scan = result[0]
                yield result

    def close(self):
        if self._pubsub is None:
            return
        self._pubsub.unsubscribe()
        self._pubsub = None
        self.scan = None
