import twiddle.check_twiddle as twiddle
from nose_parameterized import parameterized
from nose.tools import raises

import urllib2

def test_DEFAULT_TIMEOUT_is_set():
  assert twiddle.DEFAULT_TIMEOUT is not None or twiddle.DEFAULT_TIMEOUT <= 0, 'Expected that DEFAULT_TIMEOUT be integer > 0, not %s' %(twiddle.DEFAULT_TIMEOUT)

@parameterized.expand([
  ('somehost.example.com', 7002, 'bean', 'datasource', 'NumBusyConnections'),
])
def test_build_url_returns_non_empty_string(hostname, port, object_name, name, attribute_name):
  expected_val = 'http://%s:%s/twiddle/get.op?objectName=%s:name=%s&attributeName=%s' %(hostname, port, object_name, name, attribute_name)
  return_val = twiddle.build_url(hostname, object_name, name, attribute_name, port)
  assert return_val == expected_val, 'Expected that twiddle.build_url(%s) be set to "%s", not "%s"' %(expected_val, expected_val, return_val)

@parameterized.expand([
  ('somehoest.com', '7001', '', 'baz', 'baz2'),
  ('somehoest.com', '7001', '', '', 'baz2'),
  ('somehoest.com', '7001', '', '', ''),
  ('somehoest.com', '7001', None, 'baz', 'baz'),
  ('somehoest.com', '7001', 'baz', None, 'baz'),
  ('somehoest.com', '7001', 'baz', 'baz', None),
  ('somehoest.com', '7001', None, None, None),
])
@raises(ValueError)
def test_build_url_raises_ValueError(hostname, port, object_name, name, attribute_name):
  expected_val = 'http://%s:%s/twiddle/get.op?objectName=%s:name=%s&attributeName=%s' %(hostname, port, object_name, name, attribute_name)
  twiddle.build_url(hostname, object_name, name, attribute_name, port)

@parameterized.expand([
    ('',),
    (None,)
])
@raises(ValueError)
def test_build_url_should_raise_ValueError_when_hostname_is_invalid(invalid_hostname):
    uri = twiddle.build_url(invalid_hostname, 'mybean', 'myname', 'some_attribute', twiddle.DEFAULT_PORT)

@parameterized.expand([
    ('',),
    (None,),
    (0,)
])
@raises(ValueError)
def test_build_url_should_raise_ValueError_when_port_is_invalid(invalid_port):
    print("invalid_port: '%s'" %(invalid_port))
    uri = twiddle.build_url('somehoest.example.com', 'mybean', 'myname', 'some_attribute', invalid_port)

############################
#### integration tests
############################

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

