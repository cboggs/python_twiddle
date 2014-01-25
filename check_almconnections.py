###############################################################################
# Script: check_almconnections.py
# Date: 1-22-2014
# Author: Cody Lane
#
# Description:
#   This scipt will basically become a library for checking the ALM database
#   connection pool information.
#
###############################################################################

import check_twiddle as twiddle
from check_twiddle import DEFAULT_PORT

def get_database_connection_maximum(host, port=DEFAULT_PORT):
    uri = twiddle.build_url(host, 'bean', 'datasource', 'MaxPoolSize', port)
    req = twiddle.connect(uri)
    if req.getcode() == 200:
        data = req.read()
        twiddle.close(req)
        return data

def get_database_connection_minimum(host, port=DEFAULT_PORT):
    uri = twiddle.build_url(host, 'bean', 'datasource', 'MinPoolSize', port)
    req = twiddle.connect(uri)
    if req.getcode() == 200:
        data = req.read()
        twiddle.close(req)
        return data

def get_database_connection_current_used(host, port=DEFAULT_PORT):
    uri = twiddle.build_url(host, 'bean', 'datasource', 'NumBusyConnections', port)
    req = twiddle.connect(uri)
    if req.getcode() == 200:
        data = req.read()
        twiddle.close(req)
        return data

def get_database_connection_current_idle(host, port=DEFAULT_PORT):
    uri = twiddle.build_url(host, 'bean', 'datasource', 'NumIdleConnections', port)
    req = twiddle.connect(uri)
    if req.getcode() == 200:
        data = req.read()
        twiddle.close(req)
        return data

