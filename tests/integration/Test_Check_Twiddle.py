import twiddle.check_twiddle as twiddle
from nose_parameterized import parameterized
from nose.tools import raises

import urllib2

@parameterized.expand([
  ('somehost.example.com', '7001', 'bean', 'datasource', 'NumBusyConnections'),
])
def test_connect(hostname, port, object_name, name, attribute_name):
  uri = twiddle.build_url(hostname, object_name, name, attribute_name, port)
  req = twiddle.connect(uri)
  assert req is not None
  assert req.getcode() == 200

def test_close_closes_down_open_pointer():
    hostname = 'somehost.example.com'
    port = '7001'
    uri = twiddle.build_url(hostname, 'bean', 'datasource', 'NumBusyConnection', port)
    req = twiddle.connect(uri)
    twiddle.close(req)
    assert req.fp is None

