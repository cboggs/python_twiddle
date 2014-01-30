import twiddle.twiddle as twiddle
from nose_parameterized import parameterized
from nose.tools import raises

import urllib2

@parameterized.expand([
  ('localhost', '48001', 'bean', 'datasource', 'NumBusyConnections'),
])
def test_connect(hostname, port, object_name, name, attribute_name):
  uri = twiddle.build_url(hostname, object_name, name, attribute_name, port)
  req = twiddle.connect(uri)
  assert req is not None
  assert req.getcode() == 200

def test_close_closes_down_open_pointer():
    hostname = 'localhost'
    port = '48001'
    uri = twiddle.build_url(hostname, 'bean', 'datasource', 'NumBusyConnections', port)
    req = twiddle.connect(uri)
    twiddle.close(req)
    assert req.fp is None

