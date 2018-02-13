#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal
import sys
import os
import json
import logging
from conf import config
from interface import rmqclient

app = "mail2diaspora"


def configure_logging(level):

    logger.setLevel(level)

    ch = logging.StreamHandler()
    ch.setLevel(level)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s'
                                  ' - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)


def signal_handler(signal, frame):
    print('CTRL-C caught')


# configure logging
logger = logging.getLogger(__name__)
configure_logging(logging.DEBUG)

logger.info('Starting Mail_2_Diaspora application')

# start ZMQ client
if(config.rabbitmq['active']):
    c = rmqclient.start()

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C')
signal.pause()

if(config.rabbitmq['active']):
    c = rmqclient.stop()

# Exit application
logger.info('Stopping mail2diaspora application')
sys.exit(0)
