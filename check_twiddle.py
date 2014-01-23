import socket
import urllib2

DEFAULT_TIMEOUT = 5
DEFAULT_PORT    = 7001

# sets the connection timeout value
socket.setdefaulttimeout(DEFAULT_TIMEOUT)

def build_url(host, object_name, name, attribute_name, port=DEFAULT_PORT):
    '''
    Example: If attempting to construct the following:
    objectName=bean:name=datasource&attributeName=NumBusyConnections

    object_name = 'name'
    name = 'datasource'
    attribute_name = 'NumBusyConnections'

    @host           The hostname to connect to or ip address
    @port           The port number to connect to
    @object_name    The the MBean
    @name           The name of the Mbean
    @attribute_name The name of the attribute
    '''
    if host is None or host == '':
        raise ValueError('host cannot be "%s"' %(host))
    if port is None or port == '' or port <= 0:
        raise ValueError('port cannot be "%s"' %(port))
    if object_name is None or object_name == '':
        raise ValueError('object_name cannot be "%s"' %(object_name))
    if name is None or name == '':
        raise ValueError('name cannot be "%s"' %(name))
    if attribute_name is None or attribute_name == '':
        raise ValueError('attribute_name cannot be "%s"' %(attribute_name))
    uri = "http://%s:%s/twiddle/get.op?objectName=%s:name=%s&attributeName=%s" %(host, port, object_name, name, attribute_name)
    return uri

def connect(uri):
    '''
    Attempts to connect to a host:port by building a pre-canned URI.
    The request object is returned if the connection is successful.

    @uri   The URI to connect to, which should be a string like: http://www.google.com
    @host  Defaults to the global host parameter
    @port  Defaults to the global port parameter

    @raises URLError if unable to open connection or timeout is reached
    trying to connect to endpoint.
    '''
    return urllib2.urlopen(uri)

def close(request):
    '''
    @request A open url request
    '''
    request.close()

def get_max_database_connections(host, port=DEFAULT_PORT):
    uri = build_url(host, 'bean', 'datasource', 'MaxPoolSize', port)
    req = connect(uri)
    if req.getcode() == 200:
        data = req.read()
        req.close()
        return data

def get_min_database_connections(host, port=DEFAULT_PORT):
    uri = build_url(host, 'bean', 'datasource', 'MinPoolSize', port)
    req = connect(uri)
    if req.getcode() == 200:
        data = req.read()
        req.close()
        return data

def get_current_used_database_connections(host, port=DEFAULT_PORT):
    uri = build_url(host, 'bean', 'datasource', 'NumBusyConnections', port)
    req = connect(uri)
    if req.getcode() == 200:
        data = req.read()
        req.close()
        return data

def get_current_idle_database_connections(host, port=DEFAULT_PORT):
    uri = build_url(host, 'bean', 'datasource', 'NumIdleConnections', port)
    req = connect(uri)
    if req.getcode() == 200:
        data = req.read()
        req.close()
        return data

if __name__ == '__main__':
    print("used_connections: %s" %get_current_used_database_connections('somehoest.example.com'))
    print("idle_connections: %s" %get_current_idle_database_connections('somehoest.example.com'))
    print("min_connections:  %s" %get_min_database_connections('somehoest.example.com'))
    print("max_connections:  %s" %get_max_database_connections('somehoest.example.com'))

