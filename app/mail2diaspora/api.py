#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from flask import request, make_response, abort
from json import dumps
import diaspy
from mail2diaspora import app

logger = logging.getLogger(__name__)
dconfig = app.config['app']['diaspora']

@app.route("/inbox", methods=['POST'])
def new_mail():

    try:
        data = request.get_json()
        logging.debug('diapora posting: %s' % data)
        post_diaspora(data)
    except:
        logger.exception("diaspora posting failure")
        abort(400)
    return "OK"


def post_diaspora(data):

    conn = diaspy.connection.Connection(
        pod=dconfig['pod'],
        username=dconfig['username'],
        password=dconfig['password'])
    try:
        conn.login()
        stream = diaspy.streams.Stream(conn)
    except:
        logger.warn('login failure %s' % dconfig)

    from_email = data['from']
    if app.config['app']['global']['sender'] in from_email:
        message = get_message(data['parts'])
        if message:
            stream.post(message)
        else:
            logger.warn('no message found in e-mail body: %s' % data)
    else:
        logger.warn('unauthorized e-mail sender: %s' % data)


def get_message(parts):
    message = ''
    for part in parts:
        if part['content-type'] == 'text/plain':
            message = part['content']
            break
    return message


def init():
    pass
