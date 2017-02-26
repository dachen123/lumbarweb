# -*- coding: utf-8 -*-
# author:   waterpku
# company:  duoc
# date:     March, 28, 2015

import logging
import time

from nanomsg import Socket, PUB, SUB, SUB_SUBSCRIBE

from cm_web.config import load_config

config = load_config()

class EncodingFormatter(logging.Formatter):
    def __init__(self, fmt, datefmt=None, encoding=None):
        logging.Formatter.__init__(self, fmt, datefmt)
        self.encoding = encoding or 'utf-8'

    def format(self, record):
        result = logging.Formatter.format(self, record)
        if isinstance(result, unicode):
            result = result.encode(self.encoding)
        return result

class PubHandler(logging.Handler):
    """
    A basic logging handler that emits log messages through a PUB socket.

    Takes a PUB socket already bound to interfaces or an interface to bind to.

    Example::
        
        sock = context.socket(PUB)
        sock.bind("inproc://log")
        handler = PUBHandler(sock)

    Or::
        
        handler = PUBHandler("inproc://log")

    These are equivalent.

    Log messages handled by this handler are broadcase with nanomsg PUB/SUB model.

    """

    dayfmt='%Y %m %d %H:%M:%S'
    formatters = {
        logging.DEBUG: EncodingFormatter(
            "%(asctime)-15s %(name)s.%(levelname)s " +
            #    "in %(module)s [%(pathname)s:%(lineno)d]" +
                "- %(message)s\n",
            dayfmt),
        logging.INFO: EncodingFormatter(
            "%(asctime)-15s %(name)s.%(levelname)s " +
            #    "in %(module)s [%(pathname)s:%(lineno)d]" +
                "- %(message)s\n",
            dayfmt),
        logging.WARN: EncodingFormatter(
            "%(asctime)-15s %(name)s.%(levelname)s " +
            #    "in %(module)s [%(pathname)s:%(lineno)d]" +
                "- %(message)s\n",
            dayfmt),
        logging.ERROR: EncodingFormatter(
            "%(asctime)-15s %(name)s.%(levelname)s " +
            #    "in %(module)s [%(pathname)s:%(lineno)d]" +
                "- %(message)s - %(exc_info)s\n",
            dayfmt),
        logging.CRITICAL: EncodingFormatter(
            "%(asctime)-15s %(name)s.%(levelname)s " +
            #    "in %(module)s [%(pathname)s:%(lineno)d]" +
                "- %(message)s\n",
            dayfmt),
        }
    def __init__(self, pub_addr):
        logging.Handler.__init__(self)
        self.sock = Socket(PUB)
        self.sock.connect(pub_addr)
        log_level = logging.DEBUG
        self.setFormatter(PubHandler.formatters[log_level])

    def emit(self, record):
        """ Emit a log message on nanomsg pub/sub model. """
        #TODO is send asynchronous ?
        try:
            self.sock.send(self.format(record))
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def colse(self):
        self.sock.close()
        logging.Handler.close(self)

    def __del__(self):
        self.sock.close()
        # logging.Handler.__del__(self)

def add_log_handler(app, name):
    del app.logger.handlers[1:]
    nn_handler = PubHandler(app.config.get('NN_DEVICE_DICT').get(name))
    time.sleep(0.2)
    nn_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(nn_handler)
    app.logger.setLevel(1)

    #TODO   待验证正确性
    if config.MODE == 'PRODUCTION':
        from logging.handlers import SMTPHandler
        mail_handler = SMTPHandler('127.0.0.1',
                                   'server-error@duoc.cn',
                                   config.ADMINS,
                                   'Duoc Application Failed')
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(PubHandler.formatters[logging.ERROR])
        app.logger.addHandler(mail_handler)

