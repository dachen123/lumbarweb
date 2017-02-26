# -*- coding: utf-8 -*-
# author:   waterpku
# company:  duoc
# date:     March, 28, 2015

import sys
import os
from datetime import datetime



class LogWriter(object):
    """ 
    稍微封装了下写入文件的过程 
    """
    
    def __init__(self, filename=None):
        if filename:
            self.file = open(filename, "a")
            self.filename = filename
        else:
            self.file = sys.stdout
            self.filename = None

    def flush(self):
        self.file.flush()

    def write(self, content):
        self.file.write(content)
        self.file.flush()

    def writeline(self, content):
        if not content.endswith("\n"): content += "\n"
        self.file.write(content)
        self.flush()

    def writelines(self, contents):
        self.file.writelines(contents)
        self.flush()

    def archive(self):
        """ 
        接收到信号，将当前的日志文件截断存档 
        """
        try:
            if not self.filename:
                return

            #now = datetime.now()
            # rename to archive log file
            #archive_file = self.filename + now.strftime("-%Y-%m-%d")
            #if os.path.exists(archive_file):
            #    import time
            #    archive_file = "%s-%d" % (archive_file, time.time())
            self.file.close()
            #os.rename(self.filename, archive_file)
            self.file = open(self.filename, "a")
        except Exception, e:
            with open('/var/log/lumbarv2/error','a') as f:
                f.write("hello, backup log file error")

def get_writer(filename=None):
    """ 
    供log server获取writer的接口 
    """
    return LogWriter(filename)

