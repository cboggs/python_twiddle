python-daemon
=============

A simple python daemon library written by Sander Marechal stored here for my reference.  This library is based from an example in Advanced Programming in the Unix Environment, arguably one of the best books I have in my library.  Please see the link to [Sandar Marechal's site](http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/) for background on this code.

Related code for responding to IPC events
=========================================
I also wrote a signal handler library for IPC (Inter-process Communication) that was intended to work directly with this daemon.  As an example: if you wanted your daemon to respond to certain signals i.e. kill -9 for example, and perform an action when the signal is received you'll also want to check out my signal handler library.  You can register 'n' number of signals.   That code can be found at https://github.com/codylane/python-signalhandler.

