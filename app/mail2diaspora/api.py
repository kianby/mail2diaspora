#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import base64
import diaspy
from flask import request, make_response, abort
from mail2diaspora import app

logger = logging.getLogger(__name__)
authorized_sender = app.config['app']['global']['sender']
tempdir = app.config['app']['global']['tempdir']
dconfig = app.config['app']['diaspora']


@app.route("/inbox", methods=['POST'])
def new_mail():

    try:
        data = request.get_json()
        logger.debug('diapora posting: %s' % data)
        post_diaspora(data)
    except:
        logger.exception("diaspora posting failure")
        abort(400)
    return "OK"


def post_diaspora(data):

    if authorized_sender not in data['from']:
        logger.warn('unauthorized e-mail sender: %s' % data)
        return

    conn = diaspy.connection.Connection(
        pod=dconfig['pod'],
        username=dconfig['username'],
        password=dconfig['password'])
    conn.login()
    stream = diaspy.streams.Stream(conn)

    message = get_text_content(data['parts'])
    if not message:
        logger.warn('no message found in e-mail body: %s' % data)
        return

    images = []
    if 'attachments' in data:
        images = get_parts(data['attachments'], 'image/')

    # post text and image
    if images:
        if len(images) > 1:
            logger.warn('cannot post multiple images')
        else:
            # save image to disk
            image = images[0]
            image_filename = tempdir + image['filename']
            image_content = image['content'].encode('utf-8')
            with open(image_filename, 'wb') as fi:
                fi.write(base64.decodestring(image_content))

            # post text and image
            stream.post(text=message, photo=image_filename)

            # delete saved image
            os.remove(image_filename)

    # post text
    else:
        stream.post(message)


def get_text_content(parts):

    message = ''
    for part in get_parts(parts, 'text/plain'):
        message = message + part['content']
    return message


def get_parts(parts, content_type):

    matching_parts = []
    for part in parts:
        if part['content-type'].startswith(content_type):
            matching_parts.append(part)
    return matching_parts


def init():
    pass
