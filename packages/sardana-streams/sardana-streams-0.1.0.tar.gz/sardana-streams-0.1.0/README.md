# Sardana Streams

![Pypi python versions][pypi-python-versions]
![Pypi version][pypi-version]
![Pypi status][pypi-status]
![License][license]

Sardana data streaming infrastucture. Comprises:

* [x] [redis] based sardana scan recorder
* Client recorders:
  * [x] generic scan stream client (library)
  * [ ] SPEC recorder daemon
  * [ ] HDF5 recorder daemon
  * [ ] Scan GUI

## Installation

From within your favorite python environment:

```bash
$ pip install sardana-streams
```

## Usage

The name [acme](https://en.wikipedia.org/wiki/Acme_Corporation) used in the
following examples represents a fictional corporation that features prominently
in the Road Runner cartoons.

### Configuration

Activate sardana redis recorder:

* Put the installation directory where the `sardana_streams/recorder`
  resides in **RecorderPath** tango property of the MacroServer.
  (ex: `/usr/local/lib/python3.5/dist-packages/sardana_streams/recorder`)
* From spock:
  * activate the recorder with: `senv DataRecorder "['RedisRecorder']"`
  * configure the recorder with
    `senv RedisRecorder "{'host': 'acme.org', 'port': 7379, 'db': 1}"`
    (replace `host`, `port` and `db` with your own)

The `RedisRecorder` env can be a string or a dictionary identifying the Redis
database.

In case a string is given, it recognizes the same format *url* argument from
[redis.from_url()](https://redis-py.readthedocs.io/en/stable/#redis.from_url).

In case a dict is given it recognizes the same keyword arguments as
[redis.from_url()](https://redis-py.readthedocs.io/en/stable/#redis.from_url)
plus:
* `TTL`: scan time to live in seconds (defaults to **one week**)
* `key_prefix`: scan key prefix (defaults to `<macro server name>:sardana:scan`)

### Example

Here is a simple example of a client which simply listens to scan events and
prints them on screen:

```python
import contextlib

import redis
from sardana_streams.client import ScanStream

db = redis.from_url('redis://acme.org:7379/1')
prefix = "acme:sardana:scan"
stream = ScanStream(db, prefix)
with contextlib.closing(stream):
    for event in stream:
        print(event)
```

[pypi-python-versions]: https://img.shields.io/pypi/pyversions/sardana-streams.svg
[pypi-version]: https://img.shields.io/pypi/v/sardana-streams.svg
[pypi-status]: https://img.shields.io/pypi/status/sardana-streams.svg
[license]: https://img.shields.io/pypi/l/sardana-streams.svg
[redis]: https://redis.io
