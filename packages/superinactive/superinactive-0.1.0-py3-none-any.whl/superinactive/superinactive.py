#!/usr/bin/env python

# Superinactive - Supervisor plugin to monitor a file activity and restart
#              programs on inactivity
#
# Copyright (C) 2020  Dr. Volker Jaenisch
#

import os
import sys
import datetime
import time
import argparse
import signal
import threading
import pathlib
import xmlrpc.client as xmlrpclib

from supervisor import childutils

DEFAULT_TIMEOUT = 30

parser = argparse.ArgumentParser(description='Supervisor plugin to monitor a file activity and restart programs on inactivity')

monitor_group = parser.add_argument_group('file monitoring')
monitor_group.add_argument('path', metavar='path', help='file path to monitor for inactivity')
monitor_group.add_argument('timeout', metavar='timeout', type=int, help='timeout (seconds) for inactivity (default {})')

program_group = parser.add_argument_group('programs')
program_group.add_argument('program', metavar='prog', nargs='*', help="supervisor program name to restart")
program_group.add_argument('-g', '--group', action='append', default=[], help='supervisor group name to restart')
program_group.add_argument('-a', '--any', action='store_true', help='restart any child of this supervisor')


class Plugin(object):

    def __init__(self, args):
        self.args = args
        self.pre_restarting_lock = threading.Lock()
        self.restarting_lock = threading.Lock()
        self.do_monitor = True

        self.file = pathlib.Path(self.args.path)
        assert self.file.exists(), 'No such file: {self.file}'
        self.delta_time = datetime.timedelta(seconds=self.args.timeout)

        signal.signal(signal.SIGINT, self.handle_term)
        signal.signal(signal.SIGTERM, self.handle_term)
        self.rpc_init()

    def rpc_init(self):
        try:
            self.rpc = childutils.getRPCInterface(os.environ)
        except KeyError as exc:
            self.error('missing environment variable ' + str(exc))

        self.info('watching ' + self.args.path)

    def info(self, msg, file=sys.stdout):
        print('superinactive: ' + msg, file=file)
        file.flush()

    def error(self, msg, status=1):
        self.info('error: ' + msg, file=sys.stderr)
        sys.exit(status)

    def usage_error(self, msg):
        parser.print_usage(file=sys.stderr)
        self.error(msg, status=2)

    def validate_args(self, args):

        if args.program and args.any:
            self.usage_error('argument PROG not allowed with --any')
        if args.group and args.any:
            self.usage_error('argument --group not allowed with --any')
        if not args.program and not args.group and not args.any:
            self.usage_error('one of the arguments PROG --group --any is required')

    def handle_term(self, signum, frame):
        self.info('terminating')
        try:
            self.do_monitor = False
        except NameError:
            sys.exit()

    def requires_restart(self, proc):
        name = proc['name']
        group = proc['group']
        statename = proc['statename']
        pid = proc['pid']

        correct_state = (statename == 'STARTING' or statename == 'RUNNING')
        correct_name = (self.args.any or name in self.args.program or group in self.args.group)

        return correct_state and correct_name and pid != os.getpid()

    def restart_programs(self):
        self.info('restarting programs')

        procs = self.rpc.supervisor.getAllProcessInfo()
        restart_names = [proc['group'] + ':' + proc['name']
                         for proc in procs if self.requires_restart(proc)]

        for name in list(restart_names):
            try:
                self.rpc.supervisor.stopProcess(name, False)
            except xmlrpclib.Fault as exc:
                self.info('warning: failed to stop process: ' + exc.faultString)
                restart_names.remove(name)

        while restart_names:
            for name in list(restart_names):
                proc = self.rpc.supervisor.getProcessInfo(name)
                if proc['statename'] != 'STOPPED':
                    continue
                try:
                    self.rpc.supervisor.startProcess(name, False)
                    restart_names.remove(name)
                except xmlrpclib.Fault as exc:
                    self.info('warning: failed to start process: ' + exc.faultString)
                    restart_names.remove(name)
            time.sleep(0.1)

    def commence_restart(self):
        if not self.pre_restarting_lock.acquire(False):
            self.info('detected inactivity, but locked')
            return
        self.info('detected inactivity, commencing restart of programs')
        time.sleep(0.1)
        self.restarting_lock.acquire()
        self.pre_restarting_lock.release()
        self.restart_programs()
        self.restarting_lock.release()

    def file_m_time(self):
        result = self.file.stat().st_mtime
        return result

    def monitor(self):
        last_time = self.file_m_time()
        while self.do_monitor:
            time.sleep(self.args.timeout)
            self.info('file mtime: {}'.format(self.file_m_time()))
            new_time = self.file_m_time()
            if last_time == new_time:
                self.commence_restart()
            last_time = new_time


def main():
    args = parser.parse_args()
    plugin = Plugin(args)
    plugin.monitor()


if __name__ == '__main__':
    main()
