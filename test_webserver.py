#!/usr/bin/python

from __future__ import print_function
import os
import sys
import signal
import psutil
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
from SocketServer import ForkingMixIn
from signalhandler.SignalHandler import SignalHandler
from daemon import Daemon

def get_execution_path():
    abs_path = os.path.abspath(sys.argv[0])
    root_dir = os.path.dirname(abs_path)
    return root_dir

LISTEN     = ''
PORT       = 48001
PIDFILE    = get_execution_path() + '/webserver.pid'
STDOUT_LOG = get_execution_path() + '/stdout.log'
STDERR_LOG = get_execution_path() + '/stderr.log'

class MyHTTPServer(ForkingMixIn, HTTPServer):
    def __init__(self, host=LISTEN, port=PORT):
        HTTPServer.__init__(self, (host, port), MyHandler)
        self._endpoints = []
        self._sig_handler = SignalHandler()
        self.register_default_sig_handlers()

    def register_default_sig_handlers(self):
        self._sig_handler.register(signal.SIGTERM, self.stop)
        self._sig_handler.register(signal.SIGINT,  self.stop)

    def run(self):
        try:
            self.serve_forever()
        except:
            self.server_close()
            self.shutdown()

    def stop(self):
        stop_server()

    def register_endpoint(self, path):
        if path not in self._endpoints:
            self._endpoints.append(path)

class DaemonizeMyHTTPServer(Daemon):
    def run(self, server):
        if isinstance(server, MyHTTPServer) is False:
            raise ValueError('server argument must be a MyHTTPServer instance, not %s=%s' %(type(server), server))
        self.daemonize()
        server.run()

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path in self.server._endpoints:
            self.send_valid_response()
        else:
            self.send_invalid_response()

    def do_POST(self):
        pass

    def send_valid_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write('20')
        return

    def send_invalid_response(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        return

def start_server(daemonize=True):
    if daemonize:
        daemon = DaemonizeMyHTTPServer(
                pidfile = PIDFILE,
                stdin   = '/dev/null',
                stdout  = STDOUT_LOG,
                stderr  = STDERR_LOG
            )
        daemon.run(server)
    else:
        server.run()

def stop_server():
    progname = sys.argv[0]
    for proc in psutil.process_iter():
        try:
            if progname in proc.cmdline and proc.pid != os.getpid():
                os.kill(proc.pid, signal.SIGTERM)
                return True
        except:
            pass
    return False

def usage():
    print('USAGE: %s [start|stop]')
    sys.exit(0)

if __name__ == '__main__':

    try:
        action = sys.argv[1]
    except:
        usage()

    if action == 'start':
        server = MyHTTPServer(LISTEN, PORT)
        server.register_endpoint('/twiddle/get.op?objectName=bean:name=datasource&attributeName=MaxPoolSize')
        server.register_endpoint('/twiddle/get.op?objectName=bean:name=datasource&attributeName=NumBusyConnections')
        start_server()
    elif action == 'stop':
        if stop_server() is False:
            print("ERR: unable to stop server %s process" %(sys.argv[0]))
            sys.exit(1)
        sys.exit(0)
    else:
        usage()

