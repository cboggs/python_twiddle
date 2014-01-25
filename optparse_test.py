#!/usr/bin/env python

import optparse
import sys

DEFAULT_PORT='7001'

parser = optparse.OptionParser()

parser.add_option(
    '-w', 
    '--warning', 
    action='store',
    type='int',
    dest='warning', 
    metavar='WARNING', 
    help='REQUIRED: The warning threshold'
    )

parser.add_option(
    '-c',
    '--critical',
    action='store',
    type='int',
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

(options, args) = parser.parse_args()

show_usage = False
if options.critical is None:
    print('critical option is required, see usage')
    show_usage = True

if options.warning is None:
    print('warning option is required, see usage')
    show_usage = True

if options.host is None:
    print('host option is required, see usage')
    show_usage = True

if options.port is None:
    print('port option is required, see usage')
    show_usage = True

if show_usage:
    parser.print_help()
    sys.exit(1)

print('[debug] option stuff')
print('warning  =%s' %(options.warning))
print('critical =%s' %(options.critical))
print('host     =%s' %(options.host))
print('port     =%s' %(options.port))

