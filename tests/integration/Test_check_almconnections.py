import twiddle.check_almconnections as almconnections
from nose_parameterized import parameterized
from nose.tools import raises
from urllib2 import URLError

@parameterized.expand([
    ('mytesthost.com', '7001'),
])
def test_get_database_connection_maximum_returns_a_non_empty_string(host, port):
    return_val = almconnections.get_database_connection_maximum(host, port)
    assert isinstance(return_val, str), 'Expected that almconnections.get_database_connection_maximum(%s, %s) to return an integer, not %s=%s' %(host, port, type(return_val), return_val)
    assert return_val != '', 'Expected that almconnections.get_database_connection_maximum(%s, %s) to return a none empty string' %(host, port)

@parameterized.expand([
    ('mytesthost.com', '7001'),
])
def test_get_database_connection_minimum_returns_a_non_empty_string(host, port):
    return_val = almconnections.get_database_connection_minimum(host, port)
    assert isinstance(return_val, str), 'Expected that almconnections.get_database_connection_minimum(%s, %s) to return an integer, not %s=%s' %(host, port, type(return_val), return_val)
    assert return_val != '', 'Expected that almconnections.get_database_connection_minimum(%s, %s) to return a none empty string' %(host, port)

@parameterized.expand([
    ('mytesthost.com', '7001'),
])
def test_get_database_connection_current_used_returns_a_non_empty_string(host, port):
    return_val = almconnections.get_database_connection_current_used(host, port)
    assert isinstance(return_val, str), 'Expected that almconnections.get_database_connection_current_used(%s, %s) to return an integer, not %s=%s' %(host, port, type(return_val), return_val)
    assert return_val != '', 'Expected that almconnections.get_database_connection_current_used(%s, %s) to return a none empty string' %(host, port)

@parameterized.expand([
    ('mytesthost.com', '7001'),
])
def test_get_database_connection_current_idle_returns_a_non_empty_string(host, port):
    return_val = almconnections.get_database_connection_current_idle(host, port)
    assert isinstance(return_val, str), 'Expected that almconnections.get_database_connection_idle(%s, %s) to return an integer, not %s=%s' %(host, port, type(return_val), return_val)
    assert return_val != '', 'Expected that almconnections.get_database_connection_idle(%s, %s) to return a none empty string' %(host, port)
