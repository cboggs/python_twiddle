import twiddle.check_twiddle as twiddle
from nose_parameterized import parameterized
from nose.tools import raises

import urllib2

def test_DEFAULT_TIMEOUT_is_set():
  assert twiddle.DEFAULT_TIMEOUT is not None or twiddle.DEFAULT_TIMEOUT <= 0, 'Expected that DEFAULT_TIMEOUT be integer > 0, not %s' %(twiddle.DEFAULT_TIMEOUT)


def test_hostname_returns_empty_string_when_not_set():
  expected_value = ''
  return_val = twiddle.hostname
  assert return_val == expected_value, 'Expected that twiddle.hostname returns "%s", not %s' %(expected_value, return_val)

def test_hostname_returns_non_empty_string_when_set():
  return_val = twiddle.hostname
  assert return_val != '' or return_val is not None, 'Expected that twiddle.hostname to return non-empty string, not %s' %(return_val)

def test_hostname_can_be_set_to_a_string():
  expected_val = 'foobar'
  twiddle.hostname = expected_val
  return_val = twiddle.hostname
  assert return_val == expected_val, 'Expected that twiddle.host = "%s" be set to %s, not "%s"' %(expected_val, expected_val, return_val)

def test_port_sets_the_default_port_when_no_argument_is_passed():
  expected_val = twiddle.DEFAULT_PORT
  return_val = twiddle.port
  assert return_val == expected_val, 'Expected that twiddle.port be set to default %s, not %s' %(expected_val, return_val)

def test_port_sets_port_to_an_integer():
  expected_val = 7002
  twiddle.port = expected_val
  return_val = twiddle.port
  assert return_val == expected_val, 'Expected that twiddle.port = %s be set to default %s, not %s' %(expected_val, expected_val, return_val)


def test_port_returns_7001_when_using_the_default():
  expected_val = 7001
  twiddle.port = twiddle.DEFAULT_PORT
  return_val = twiddle.port
  assert return_val == expected_val, 'Expected that twiddle.port be set to default %s, not %s' %(expected_val, return_val)

@parameterized.expand([
  ('somehost.example.com', 7002, 'bean', 'datasource', 'NumBusyConnections'),
])
def test_build_url_returns_non_empty_string(hostname, port, object_name, name, attribute_name):
  expected_val = 'http://%s:%s/twiddle/get.op?objectName=%s:name=%s&attributeName=%s' %(hostname, port, object_name, name, attribute_name)
  twiddle.hostname = hostname
  twiddle.port = port
  return_val = twiddle.build_url(object_name, name, attribute_name)
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
  twiddle.hostname = hostname
  twiddle.port = port
  twiddle.build_url(object_name, name, attribute_name)

@parameterized.expand([
  ('qd-app-10.rally.prod', '7001', 'bean', 'datasource', 'NumBusyConnections'),
])
def test_urlopen(hostname, port, object_name, name, attribute_name):
  twiddle.hostname = hostname
  twiddle.port = port
  uri = twiddle.build_url(object_name, name, attribute_name)
  req = urllib2.urlopen(uri)
  response = req.read()
  print('response=%s, code=%s' %(response, req.getcode()))
  print(dir(req))


@parameterized.expand([
  ('qd-app-10.rally.prod', '7001', 'bean', 'datasource', 'NumBusyConnections'),
])
def test_connect(hostname, port, object_name, name, attribute_name):
  req = twiddle.connect(object_name, name, attribute_name, hostname, port)
  assert req is not None
  assert req.getcode() == 200
