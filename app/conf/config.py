#!/usr/bin/env python
# -*- coding: utf-8 -*-

import profig

# constants
TEMP = "main.tempdir"

MAIL_POLLING = "mail.fetch_polling"
MAILER_URL = "mail.mailer_url"

DIASPORA_POD = "diaspora.pod"
DIASPORA_USERNAME = "diaspora.username"
DIASPORA_PASSWORD = "diaspora.password"


# variable
params = dict()


def initialize(config_pathname):
    cfg = profig.Config(config_pathname)
    cfg.sync()
    params.update(cfg)


def get(key):
    return params[key]


def getInt(key):
    return int(params[key])


def _str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def getBool(key):
    return _str2bool(params[key])

