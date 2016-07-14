#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import json
import logging
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)


def load_config():
    """ load global config from json file
    """
    config_path = os.environ['CONFIG_PATHNAME']
    logger.info('Load config from %s' % config_path)
    with open(config_path, 'rt') as config_file:
        config = json.loads(config_file.read())
        return config


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


def get_entire_config():
    return config


def get_config(section, param, value=None):
    try:
        value = config[section][param]
    except:
        logger.warn('missing config param %s.%s' % (section, param))
    return value

# configure logging
logger = logging.getLogger(__name__)
configure_logging(logging.DEBUG)

# load on-disk configuration
config = load_config()

# configure flask
config['global']['cwd'] = os.getcwd()
config['runtime'] = {}
config['runtime']['exit_code'] = 0
app.config['app'] = config

app.wsgi_app = ProxyFix(app.wsgi_app)

# initialize API
from mail2diaspora import api
api.init()

logger.info('Starting Mail_2_Diaspora application')

app.run(host=config['http']['host'],
        port=config['http']['port'],
        debug=False, use_reloader=False)

# Exit application
exit_code = config['runtime']['exit_code']
logger.info('Stopping Mail_2_Diaspora application (%d)' % exit_code)
sys.exit(exit_code)
