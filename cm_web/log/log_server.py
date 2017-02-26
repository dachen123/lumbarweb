#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:   waterpku
# company:  duoc
# date:     March, 28, 2015

import signal

import argparse
# import nanomsg
from nanomsg import Socket, PUB, SUB, SUB_SUBSCRIBE

from cm_web.log.log_writer import get_writer

from cm_web.config import load_config

class LogRecorder(object):
    """
    """

    def __init__(self, log_file, sub_addr):
        """ args:
            ::log_file::
                日志文件名
            ::sub_addrs::
                订阅的nanomsg频道列表，暂时先不用，先用内置的列表
        """
        self.log_file = log_file
        self.sub_addr = sub_addr

    def init(self):
        self.writer = get_writer(self.log_file)
        self.socket = Socket(SUB)
        self.socket.set_string_option(SUB, SUB_SUBSCRIBE, "")
        self.socket.bind(self.sub_addr)

    def run(self):
        while True:
            try:
                string = self.socket.recv()
                self.writer.writeline(string)
            except Exception as e:
                print e

    def close(self):
        self.socket.close()

    def archive(self, signal_number, stack_frame):
        self.writer.archive()
        return None

    def __del__(self):
        self.close()


parser = argparse.ArgumentParser(description = __doc__)
parser.add_argument("-f", "--filename", dest="file",
        default=None,
        help="The file to record the log")
parser.add_argument("-a", "--address", dest="addr", 
        default=None,
        help="The subscribe address")
parser.add_argument("-d", "--daemon", dest="daemon", action="store_true",
        help="run as a daemon")
parser.add_argument("-u", "--unittest", dest="utest", action="store_true",
        default=False, help="run as unittest")

if __name__ == "__main__":
    
    args = parser.parse_args()
    utest = args.utest
    config = load_config(utest)
    filename = args.file or ("%s.log" % config.LOGGER_NAME)

    logbackupdir = config.LOG_BACKUP_DIR
    sub_addr = args.addr or config.NN_DEVICE_DICT[config.LOGGER_NAME]
    as_daemon = args.daemon
    if not as_daemon:
        recorder = LogRecorder(filename, sub_addr)
        recorder.init()
        recorder.run()
    else:
        import daemon
        import time
        from datetime import datetime
        from lockfile.pidlockfile import PIDLockFile
        recorder = LogRecorder(filename, sub_addr)
        # selflog = open(logbackupdir + "recorder-log-%d" % 
        #         int(time.time()), "w+")
        selflog = open(logbackupdir + \
                datetime.now().strftime("recorder-log-%Y-%m-%d") ,"w+")
        context = daemon.DaemonContext(
                working_directory=config.LOG_DIR,
                pidfile=PIDLockFile(config.LOG_PID),
                stderr = selflog,
                stdout = selflog,
                files_preserve=[selflog]
        )

        context.signal_map.update({
            signal.SIGUSR1: recorder.archive,
            signal.SIGUSR2: None,
        })
        with context:
            recorder.init()
            recorder.run()
    
