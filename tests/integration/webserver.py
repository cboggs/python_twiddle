#!/usr/bin/env python

import SimpleHTTPServer
import SocketServer

LISTEN = ""
PORT   = 48001

Handler  = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer((LISTEN, PORT), Handler)

def start():
    httpd.serve_forever()

def stop():
    httpd.server_close()
