#!/usr/bin/env python

from __future__ import print_function
import twiddle
import sys

def get_database_connection_maximum(host, port=twiddle.DEFAULT_PORT):
    '''
    Returns the current maximum total connections for the database pool.
    '''
    result = twiddle.connect_factory(host, 'bean', 'datasource', 'MaxPoolSize', port)
    return int(result)

def get_database_connection_minimum(host, port=twiddle.DEFAULT_PORT):
    '''
    Returns the current minim total connections for the database pool.
    '''
    result = twiddle.connect_factory(host, 'bean', 'datasource', 'MinPoolSize', port)
    return int(result)

def get_database_connection_current_used(host, port=twiddle.DEFAULT_PORT):
    '''
    Returns the current number of used total connections for the database pool.'
    '''
    result = twiddle.connect_factory(host, 'bean', 'datasource', 'NumBusyConnections', port)
    return int(result)

def get_database_connection_current_idle(host, port=twiddle.DEFAULT_PORT):
    '''
    Returns the current number of idle total connections for the database pool.'
    '''
    result = twiddle.connect_factory(host, 'bean', 'datasource', 'NumIdleConnections', port)
    return int(result)

def calculate_percentage_used(host, port=twiddle.DEFAULT_PORT, decimals=0):
    '''
    Calculate the percentage of used database connections based from
    the maximum and calculate the result to the nearest decimal.
    
    Due to the way rounding works in binary form it is not a bug that
    if you wanted the result to be 1.6, with one decimal it cannot be 
    represented as 1.6, instead the result would be 1.6000000000000001
    '''
    if decimals < 0: decimals = 0
    max = float(get_database_connection_maximum(host, port))
    used = float(get_database_connection_current_used(host, port))
    result = (used / max) * 100
    return round(result, decimals)

def calculate_percentage_idle(host, port=twiddle.DEFAULT_PORT, decimals=0):
    '''
    Calculate the percentage of idle database connections based from
    the maximum and calculate the result to the nearest decimal.

    Due to the way rounding works in binary form it is not a bug that
    if you wanted the result to be 1.6, with one decimal it cannot be 
    represented as 1.6, instead the result would be 1.6000000000000001
    '''
    max = float(get_database_connection_maximum(host, port))
    idle = float(get_database_connection_current_idle(host, port))
    result = (idle / max) * 100
    return round(result, decimals)

def validate_required_options():
    '''
    Ensures that all required command line options are present.
    If not, exits with error message.
    '''
    # check for required options
    if options.host is None:
        print('ERR: required option --host', file=sys.stderr)
        sys.exit(1)

    if options.port is None:
        print('ERR: required option --port', file=sys.stderr)
        sys.exit(1)

def add_additional_options():
    parser = twiddle.create_default_cmdline_options()

    parser.add_option(
            '--max-connections',
            action='store_true',
            default=False,
            metavar='MAXCONNECTIONS',
            dest='maxconnections',
            help='Returns the amount of maximum connections'
        )

    parser.add_option(
            '--min-connections',
            action='store_true',
            default=False,
            metavar='MINCONNECTIONS',
            dest='minconnections',
            help='Returns the amount of minimum connections'
        )

    parser.add_option(
            '--idle-connections',
            action='store_true',
            default=False,
            metavar='IDLECONNECTIONS',
            dest='idleconnections',
            help='Returns the amount of idle connections if ' \
                    '-w and -c are not present. ' \
                    'Otherise this option is required with -w and -c'
        )

    parser.add_option(
            '--used-connections',
            action='store_true',
            default=False,
            metavar='USEDCONNECTIONS',
            dest='usedconnections',
            help='Returns the amount of used connections if ' \
                    '-w and -c are not present. ' \
                    'Otherwise this option is required with -w and -c'
        )

    parser.add_option(
            '--idle-connection-percent',
            action='store_true',
            default=False,
            metavar='IDLECONNECTIONPERCENT',
            dest='idleconnectionpercent',
            help='Returns the percentage amount of idle connections'
        )

    parser.add_option(
            '--used-connection-percent',
            action='store_true',
            default=False,
            metavar='USEDCONNECTIONPERCENT',
            dest='usedconnectionpercent',
            help='Returns the percentage amount of used connections'
        )

    parser.add_option(
            '--operator',
            action='store_action',
            default='>=',
            metavar='OPERATOR',
            dest='operator',
            help='Sets the operator that is used when calculating thresholds'
        )

    return parser

def critical_alarm(alarm_type, datasource, operator, retrieved_value, tresh_value):
    '''
    Constructs a critical alarm message that would look like the following

    alarm_type --------|
    datasource --------|---------|
    operator ----------|---------|----------------------------|------------------|
    retrieved_value ---|---------|----------------------------|--------------|   |
    thresh_value ------|---------|----------------------------|--------------|---|--|
                       V         V                            V              V   V  V
    CRITICAL: The percentage of used database connections is >= threshold [60.0 >= 40]

    @alarm_type       The type of the alarm, example [percentage, number]
    @datasource       The datasource attribute for the alarm: example [used]
    @operator         The boolean operator for the alarm in string form, example: [>=, <=, <, >]
    @retrieved_value  The retrieved value that we got from the endpoint, example [60.0]
    @thres_value      The threshold value that was breached, example: [40]
    '''
    print('CRITICAL: The %s of %s database connections is %s threshold [%s %s %s]' \
            %(alarm_type, datasource, operator, retrieved_value, operator, tresh_value),\
            file=sys.stderr)

def warning_alarm(alarm_type, datasource, operator, retrieved_value, tresh_value):
    '''
    Constructs a warning alarm message that would look like the following

    alarm_type --------|
    datasource --------|---------|
    operator ----------|---------|----------------------------|------------------|
    retrieved_value ---|---------|----------------------------|--------------|   |
    thresh_value ------|---------|----------------------------|--------------|---|--|
                       V         V                            V              V   V  V
    WARNING: The percentage of used database connections is >= threshold [60.0 >= 40]

    @alarm_type       The type of the alarm, example [percentage, number]
    @datasource       The datasource attribute for the alarm: example [used]
    @operator         The boolean operator for the alarm in string form, example: [>=, <=, <, >]
    @retrieved_value  The retrieved value that we got from the endpoint, example [60.0]
    '''
    print('WARNING: The %s of %s database connections is %s threshold [%s %s %s]' \
            %(alarm_type, datasource, operator, retrieved_value, operator, tresh_value),
            file=sys.stderr)

def process_thresholds(crit_thresh, warn_thresh, idle_pcnt, used_pcnt, used, idle):
    '''
    '''
    calc_crit_percentage = False
    calc_warn_percentage = False

    if crit_thresh is not None:
        calc_crit_percentage = crit_thresh.endswith('%')
        crit_thresh = int(crit_thresh.rstrip('%'))
    if warn_thresh is not None:
        calc_warn_percentage = warn_thresh.endswith('%')
        warn_thresh = int(warn_thresh.rstrip('%'))

    print('DEBUG: crit_treshold ', crit_thresh, ' calc_crit_percentage ', calc_crit_percentage)
    print('DEBUG: warn_treshold ', warn_thresh, ' calc_warn_percentage ', calc_warn_percentage)

    if calc_crit_percentage:
        print('DEBUG: calculating critical threshold percentages')
        print('DEBUG: used_pcnt ', used_pcnt)
        print('DEBUG: idle_pcnt ', idle_pcnt)
        if used_pcnt and used_pcnt >= crit_thresh:
            critical_alarm('percentage', 'used', '>=', used_pcnt, crit_thresh)
            sys.exit(2)
        elif idle_pcnt and idle_pcnt >= crit_thresh:
            critical_alarm('percentage', 'idle', '>=', idle_pcnt, crit_thresh)
            sys.exit(2)
    else:
        print('DEBUG: calculating critical threshold numbers')
        print('DEBUG: used ', used)
        print('DEBUG: idle ', idle)
        if used and used >= crit_thresh:
            critical_alarm('number', 'used', '>=', used, crit_thresh)
            sys.exit(2)
        elif idle and idle >= crit_thresh:
            critical_alarm('number', 'idle', '>=', idle, crit_thresh)
            sys.exit(2)

    if calc_warn_percentage:
        print('DEBUG: calculating warning threshold percentages')
        print('DEBUG: used_pcnt ', used_pcnt)
        print('DEBUG: idle_pcnt ', idle_pcnt)
        if used_pcnt and used_pcnt >= warn_thresh:
            warning_alarm('percentage', 'used', '>=', used_pcnt, warn_thresh)
            sys.exit(1)
        elif idle_pcnt and idle_pcnt >= warn_thresh:
            warning_alarm('percentage', 'idle', '>=', idle_pcnt, warn_thresh)
            sys.exit(1)
    else:
        print('DEBUG: calculating warning threshold numbers')
        print('DEBUG: used ', used)
        print('DEBUG: idle ', idle)
        if used and used >= warn_thresh:
            warning_alarm('percentage', 'used', '>=', used, warn_thresh)
            sys.exit(1)
        elif idle and idle >= warn_thresh:
            warning_alarm('percentage', 'idle', '>=', idle, warn_thresh)
            sys.exit(1)

decimals = 0
parser = add_additional_options()
(options, args) = parser.parse_args()

# ensure all required options are present
validate_required_options()

cmdline_results = {}
cmdline_results['max']   = None
cmdline_results['min']   = None
cmdline_results['used']  = None
cmdline_results['idle']  = None
cmdline_results['idle%'] = None
cmdline_results['used%'] = None
cmdline_results['warning']  = options.warning
cmdline_results['critical'] = options.critical

if options.maxconnections:
    cmdline_results['max'] = get_database_connection_maximum(options.host)

if options.minconnections:
    cmdline_results['min'] = get_database_connection_minimum(options.host)

if options.usedconnections:
    cmdline_results['used'] = get_database_connection_current_used(options.host)

if options.idleconnections:
    cmdline_results['idle'] = get_database_connection_current_idle(options.host)

if options.idleconnectionpercent:
    cmdline_results['idle%'] = calculate_percentage_idle(options.host, options.port, decimals)

if options.usedconnectionpercent:
    cmdline_results['used%'] = calculate_percentage_used(options.host, options.port, decimals)

if options.warning or options.critical:
    if options.warning.endswith('%s') or options.critical.endswith('%'):
        if cmdline_results.get('used%') is None:
            cmdline_results['used%'] = calculate_percentage_used(options.host, options.port, decimals)
        if cmdline_results.get('idle%') is None:
            cmdline_results['idle%'] = calculate_percentage_idle(options.host, options.port, decimals)

    if options.warning or options.critical:
        process_thresholds( \
            crit_thresh = cmdline_results.get('critical'), \
            warn_thresh = cmdline_results.get('warning'), \
            idle_pcnt   = cmdline_results.get('idle%'), \
            used_pcnt   = cmdline_results.get('used%'), \
            used        = cmdline_results.get('used'), \
            idle        = cmdline_results.get('idle')
        )

#if cmdline_results.get('idle') is None and cmdline_results.get('used') is None:
#    print('ERR: You cannot specify a warning percentage without --idle-connections or --used-connections')
#    sys.exit(1)

print(cmdline_results)

