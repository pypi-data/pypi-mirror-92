"""
Store sardana scans in a redis DB.

<prefix> refers to the macroserver name + ":sardana" (Ex: "bl04:sardana")

A specific scan will have the following structure:

<prefix>
  |- scan           (stores list of completed scan keys <prefix>:scan:<scan_nb>:<index>)
     |- counter     (stores scan gid - an always increasing counter)
     |- <scan nb>   (stores index - an always increasing counter for a <scan nb>
        |- <index>           (stores scan meta information (msgpack))
           |- points         (stores nb. of points recorded) (has TTL)
              |- <pt. nb>    (stores nb. of events for this point nb(*)) (has TTL)
                 |- <ev. nb> (stores point data (msgpack)) (has TTL)

(*) a point may have more than one event if processed data is registered
    at a later time
"""

import msgpack

from sardana_streams.redis import to_redis, Redis, pack


START_SCRIPT = """
local scan = ARGV[1]
local scan_nb = ARGV[2]
local header_packed = ARGV[3]
local expire = ARGV[4]
local key_scan_counter = scan .. ':counter'
local gid = redis.call('incr', key_scan_counter)
local key_sn = scan .. ':' .. scan_nb
local id = redis.call('incr', key_sn)
local key_scan = key_sn .. ':' .. id
local key_points = key_scan .. ':points'
redis.call('set', key_scan, header_packed)
redis.call('setex', key_scan .. ':points', expire, 0)
redis.call('publish', scan, key_scan .. '|header|' .. header_packed)
return key_scan
"""


END_SCRIPT = """
local key_scan = KEYS[1]
local scan = ARGV[1]
local tail_packed = ARGV[2]
local tail = cmsgpack.unpack(tail_packed)
local meta_packed = redis.call('get', key_scan)
local meta = cmsgpack.unpack(meta_packed)
for k, v in pairs(tail) do
  meta[k] = v
end
meta['__version__'] = 1
redis.call('set', key_scan, cmsgpack.pack(meta))
redis.call('rpush', scan, key_scan)
redis.call('publish', scan, key_scan .. '|tail|' .. tail_packed)
return key_scan
"""


RECORD_SCRIPT = """
local key_scan = KEYS[1]
local scan = ARGV[1]
local record_nb = ARGV[2]
local record_packed = ARGV[3]
local expire = ARGV[4]
local key_points = key_scan .. ":points"
local key_record_id = key_points .. ":" .. record_nb
local nb = redis.call('incr', key_record_id)
local key_record = key_record_id .. ':' .. nb
if expire == nil then
  local expire_ms = redis.call('pttl', key_points)
  redis.call('pexpire', key_record_id, expire_ms)
  redis.call('psetex', key_record, expire_ms, record_packed)
else
  redis.call('setex', key_record, expire, record_packed)
end
if nb == 0 then
  redis.call('incr', key_points)
end
redis.call('publish', scan, key_record .. '|record|' .. record_packed)
return key_record
"""


class ScanRecorder:

    TTL = 60 * 60 * 24 * 7    # one week

    def __init__(self, redis, prefix, ttl=TTL):
        self._init(redis, prefix, ttl)

    def __getstate__(self):
        db = self._db
        if isinstance(db, Redis):
            db = db.connection_pool.connection_kwargs
        return dict(db=db, prefix=self.prefix, ttl=self.ttl, scan_key=self.scan_key)

    def __setstate__(self, state):
        self._init(**state)

    def _init(self, db, prefix, ttl, scan_key=None):
        self._db = db
        self.redis = to_redis(db)
        self.prefix = prefix
        self.ttl = ttl
        self.scan_key = scan_key
        self._start = self.redis.register_script(START_SCRIPT)
        self._end = self.redis.register_script(END_SCRIPT)
        self._record = self.redis.register_script(RECORD_SCRIPT)

    def start(self, header):
        sn = header['serialno']
        start = dict(title=header['title'],
                     macro_name=header['title'].split(' ', 1)[0],
                     ref_moveables=header['ref_moveables'],
                     counters=header['counters'],
                     sample=header['SampleInfo'],
                     source=header['SourceInfo'],
                     pre_snapshot=header['preScanSnapShot'],
                     uid=header['macro_id'],
                     scan_dir=header['ScanDir'],
                     scan_file=header['ScanFile'],
                     start_ts=header['startts'],
                     total_scan_intervals=header['total_scan_intervals'],
                     total_nb_points=header['total_scan_intervals']+1,
                     scan_nb=header['serialno'],
                     columns=header['datadesc'],
                     user=header['user'],
                     __version__=1)
        # use pure msgpack: redis lua script will read from it
        args = self.prefix, sn, msgpack.packb(start), self.ttl
        self.scan_key = self._start(args=args)
        return self.scan_key

    def end(self, tail):
        data = dict(end_ts=tail['endts'],
                    end_status=tail['endstatus'])
        # use pure msgpack: redis lua script will read from it
        args = self.prefix, msgpack.packb(data)
        return self._end(keys=(self.scan_key,), args=args)

    def record(self, point_nb, record, ttl=None):
        if ttl is None:
            args = self.prefix, point_nb, pack(record)
        else:
            args = self.prefix, point_nb, pack(record), ttl
        return self._record(keys=(self.scan_key,), args=args)
