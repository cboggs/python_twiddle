#!/usr/bin/env python
###############################################################################
# Script: twiddle.py
# Date: 1-22-2014
# Author: Cody Lane
#
# Description:
#   An example that uses the urllib2 python library for connecting to a java
#   twiddle endpoint.  A twiddle endpoint listens for HTTP GET requests
#   that contain JMX information.
#
#   The use of Jconsole is/will be required first to obtain the JXM MBean
#   information so you can plug in this information to the script.
#
###############################################################################
from __future__ import print_function
import socket
import urllib2
from urllib2 import URLError
from optparse import OptionParser
import sys

DEFAULT_TIMEOUT = 5
DEFAULT_PORT    = 7001

# sets the connection timeout value
socket.setdefaulttimeout(DEFAULT_TIMEOUT)

def connect_factory(host, object_name, name, attribute_name, port=DEFAULT_TIMEOUT):
    try:
       uri = build_url(host, object_name, name, attribute_name, port) 
    except ValueError, e:
        print('ERR: %s' %(e), file=sys.stderr)
        sys.exit(1)

    try:
        req = connect(uri)
        if req.getcode() == 200:
            data = req.read()
            close(req)
            return data
    except URLError, e:
        print('ERR: %s' %(e), file=sys.stderr)
        sys.exit(1)

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

def create_default_cmdline_options():
    '''
    Creates some default options that we can use in subclasses?
    '''
    parser = OptionParser()

    parser.add_option(
        '-w',
        '--warning',
        action='store',
        type='string',
        dest='warning',
        metavar='WARNING',
        help='REQUIRED: The warning threshold'
        )

    parser.add_option(
        '-c',
        '--critical',
        action='store',
        type='string',
        dest='critical',
        metavar='CRITICAL',
        help='REQUIRED: The critical threshold'
        )

    parser.add_option(
        '-H',
        '--host',
        action='store',
        type='string',
        dest='host',
        metavar='HOST',
        help='REQUIRED: The hostname/ip address'
        )

    parser.add_option(
        '-p',
        '--port',
        action='store',
        type='string',
        dest='port',
        metavar='PORT',
        help='REQUIRED: The twiddle port to connect to, defaults to %s' %(DEFAULT_PORT),
        default=DEFAULT_PORT
         )

    return parser

if __name__ == "__main__":
    (options, args) = create_default_cmdline_options() 
    print(options)
    print(args)

