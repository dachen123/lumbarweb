#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:   waterpku
# company:  duoc
# date:     March, 28, 2015

import os
import signal
import string

f = open('/var/lib/dc_log/rec.pid', 'r')
pid = f.read()
print pid
os.kill(string.atoi(pid), signal.SIGUSR1)
f.close()
