import twiddle.check_almconnections as almconnections
from nose_parameterized import parameterized
from nose.tools import raises
from urllib2 import URLError

@parameterized.expand([
    ('', ''),
    (None, None),
    ('', None),
    (None, ''),
    (None, 0),
])
@raises(ValueError)
def test_get_database_connection_maximum_raises_ValueError_when_arguments_are_invalid(invalid_hostname, invalid_port):
    almconnections.get_database_connection_maximum(invalid_hostname, invalid_port)

@parameterized.expand([
    ('nonexistant.hostname', '80'),
])
@raises(URLError)
def test_get_database_connection_maximum_raises_ValueError_when_arguments_are_invalid(invalid_hostname, invalid_port):
    almconnections.get_database_connection_maximum(invalid_hostname, invalid_port)

@parameterized.expand([
    ('', ''),
    (None, None),
    ('', None),
    (None, ''),
    (None, 0),
])
@raises(ValueError)
def test_get_database_connection_minimum_raises_ValueError_when_arguments_are_invalid(invalid_hostname, invalid_port):
    almconnections.get_database_connection_minimum(invalid_hostname, invalid_port)

@parameterized.expand([
    ('nonexistant.hostname', '80'),
])
@raises(URLError)
def test_get_database_connection_minimum_raises_ValueError_when_arguments_are_invalid(invalid_hostname, invalid_port):
    almconnections.get_database_connection_minimum(invalid_hostname, invalid_port)

@parameterized.expand([
    ('', ''),
    (None, None),
    ('', None),
    (None, ''),
    (None, 0),
])
@raises(ValueError)
def test_get_database_connection_current_used_raises_ValueError_when_arguments_are_invalid(invalid_hostname, invalid_port):
    almconnections.get_database_connection_current_used(invalid_hostname, invalid_port)

@parameterized.expand([
    ('nonexistant.hostname', '80'),
])
@raises(URLError)
def test_get_database_connection_current_used_raises_ValueError_when_arguments_are_invalid(invalid_hostname, invalid_port):
    almconnections.get_database_connection_current_used(invalid_hostname, invalid_port)

@parameterized.expand([
    ('', ''),
    (None, None),
    ('', None),
    (None, ''),
    (None, 0),
])
@raises(ValueError)
def test_get_database_connection_current_idle_raises_ValueError_when_arguments_are_invalid(invalid_hostname, invalid_port):
    almconnections.get_database_connection_current_idle(invalid_hostname, invalid_port)

@parameterized.expand([
    ('nonexistant.hostname', '80'),
])
@raises(URLError)
def test_get_database_connection_current_idle_raises_ValueError_when_arguments_are_invalid(invalid_hostname, invalid_port):
    almconnections.get_database_connection_current_idle(invalid_hostname, invalid_port)

