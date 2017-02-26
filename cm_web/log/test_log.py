#!/usr/bin/env python
# -*- coding: utf-8 -*-
############################################################################
#  
#    Author: waterpku
#    Date:   2015-3-28
#
############################################################################

import logging
import time
from logging import NOTSET
from duoc.log.dclogging import PubHandler
from duoc.config import load_config

config = load_config(test=True)

logger = logging.getLogger(config.LOGGER_NAME)
handler = PubHandler(config.NN_DEVICE_DICT['test'])
time.sleep(1)
#handler = logging.StreamHandler()
handler.setLevel(NOTSET)
logger.addHandler(handler)
logger.setLevel(NOTSET)
logger.info("this is an info message")
logger.debug("this is a debug message")
logger.warning("this is a warning message")
logger.error("this is an error message")
logger.critical("this is a critical message")
try:
    num = 1 / 0
except Exception as ex:
    logger.exception("this is an exception message")
