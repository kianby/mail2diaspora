#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import base64
import diaspy
import os
from threading import Thread
from conf import config
from core import mailer
from util.fun import cron

logger = logging.getLogger(__name__)


def post_diaspora(data):

    posted = False

    conn = diaspy.connection.Connection(
        pod=config.get(config.DIASPORA_POD),
        username=config.get(config.DIASPORA_USERNAME),
        password=config.get(config.DIASPORA_PASSWORD),
    )
    conn.login()
    stream = diaspy.streams.Stream(conn)

    message = get_text_content(data["parts"])
    if not message:
        logger.warn("no message found in e-mail body: %s" % data)
        return

    images = []
    if "attachments" in data:
        images = get_parts(data["attachments"], "image/")

    # post text and image
    if images:
        if len(images) > 1:
            logger.warn("cannot post multiple images")
        else:
            # save image to disk
            image = images[0]
            image_filename = image["filename"]
            image_content = image["content"].encode("utf-8")
            with open(image_filename, "wb") as fi:
                fi.write(base64.decodestring(image_content))

            # post text and image
            stream.post(text=message, photo=image_filename)
            posted = True

            # delete saved image
            os.remove(image_filename)

    # post text
    else:
        stream.post(message)
        posted = True

    if posted:
        mailer.send(data["from"], "RE: " + data["subject"], message)


def get_text_content(parts):
    message = ""
    for part in get_parts(parts, "text/plain"):
        message = message + part["content"]
    return message


def get_parts(parts, content_type):
    matching_parts = []
    for part in parts:
        if part["content-type"].startswith(content_type):
            matching_parts.append(part)
    return matching_parts


@cron
def mail_poll():
    for msg in mailer.fetch():
        if msg["subject"].upper() == "DIASPORA":
            data = mailer.get(msg["id"])
            try:
                post_diaspora(data["email"])
                mailer.delete(msg["id"])
            except:
                logger.exception("post exception")

