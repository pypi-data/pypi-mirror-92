from sardana.macroserver.scan.recorder import DataRecorder

from sardana_streams.redis import to_redis
from sardana_streams.recorder.scan import ScanRecorder


class RedisRecorder(DataRecorder):
    """
    Sardana Redis recorder

    Activate with:

    * Put the directory where this file resides in RecorderPath MacroServer
      tango property
    * senv DataRecorder "['RedisRecorder']"
    * senv RedisRecorder "{'host': 'acme.org', 'port': 7379, 'db': 1}"
    """

    #: Default TTL to one week
    TTL = 60 * 60 * 24 * 7

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        macro = kwargs['macro']
        recorder_kwargs = macro.getEnv('RedisRecorder')
        ttl = recorder_kwargs.pop('TTL', self.TTL)
        key_prefix = recorder_kwargs.pop('key_prefix', None)
        redis = to_redis(recorder_kwargs)
        if key_prefix is None:
            ms_name = macro.getMacroServer().get_name().lower()
            key_prefix = '{}:sardana:scan'.format(ms_name)
        self.redis_scan = ScanRecorder(redis, key_prefix, ttl)

    def _startRecordList(self, recordlist):
        header = dict(recordlist.getEnviron())
        header['datadesc'] = [col.toDict() for col in header['datadesc']]
        snapshot = []
        for col in header.get('preScanSnapShot', ()):
            data = col.toDict()
            try:
                data['value'] = col.pre_scan_value
            except AttributeError:
                data['value'] = None
            snapshot.append(data)
        header['preScanSnapShot'] = snapshot
        self.datadesc = list(header['datadesc'])
        return self.redis_scan.start(header)

    def _endRecordList(self, recordlist):
        tail = dict(recordlist.getEnviron())
        tail['datadesc'] = [col.toDict() for col in tail['datadesc']]
        self.redis_scan.end(tail)

    def _writeRecord(self, record):
        self.redis_scan.record(record.recordno, record.data)
