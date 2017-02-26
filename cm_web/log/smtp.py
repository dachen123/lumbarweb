#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:   waterpku
# company:  duoc
# date:     March, 28, 2015

import logging
from duoc.config import load_config

config = load_config()

def get_logger():
    logger = logging.getLogger()

    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler('127.0.0.1',
                               'server-error@duoc.cn',
                               config.ADMINS,
                               'Duoc Application Failed')
    mail_handler.setLevel(logging.ERROR)
    logger.addHandler(mail_handler)
    return logger

if __name__ == '__main__':
    logger = get_logger()
    logger.error('this is a test mail for logging')

