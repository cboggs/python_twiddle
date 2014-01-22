import socket
import urllib2

DEFAULT_TIMEOUT = 5
DEFAULT_PORT    = 7001

hostname = ''
port     = DEFAULT_PORT

# sets the connection timeout value
socket.setdefaulttimeout(DEFAULT_TIMEOUT)

def build_url(object_name, name, attribute_name):
  '''
  Example: If attempting to construct the following:
  objectName=bean:name=datasource&attributeName=NumBusyConnections

  object_name = 'name'
  name = 'datasource'
  attribute_name = 'NumBusyConnections'

  @object_name    The the MBean
  @name           The name of the Mbean
  @attribute_name The name of the attribute
  '''
  if object_name is None or object_name == '':
    raise ValueError('object_name cannot be undefined')
  elif name is None or name == '':
    raise ValueError('name cannot be undefined')
  elif attribute_name is None or attribute_name == '':
    raise ValueError('attribute_name cannot be undefined')

  uri = "http://%s:%s/twiddle/get.op?objectName=%s:name=%s&attributeName=%s" %(hostname, port, object_name, name, attribute_name)
  return uri

def connect(object_name, name, attribute_name, host=hostname, host_port=port):
  global hostname
  hostname = host
  global port
  port = host_port
  uri = build_url(object_name, name, attribute_name)
  return urllib2.urlopen(uri)
