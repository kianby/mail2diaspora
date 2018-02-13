#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika
import json
import logging
import re
import subprocess
from threading import Thread
from conf import config

logger = logging.getLogger(__name__)


def get_rabbitmq_connection():
    credentials = pika.PlainCredentials(
        config.rabbitmq['username'], config.rabbitmq['password'])
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.rabbitmq['host'], port=config.rabbitmq[
                                         'port'], credentials=credentials, virtual_host=config.rabbitmq['vhost']))
    return connection


def mail(to_email, subject, message):

    body = {
        'to': to_email,
        'subject': subject,
        'content': message
    }
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    channel.basic_publish(exchange=config.rabbitmq['exchange'],
                          routing_key='mail.command.send',
                          body=json.dumps(body, indent=False, sort_keys=False))
    connection.close()
    logger.info('Email for %s posted' % to_email)


def send_delete_command(content):

    connection = get_rabbitmq_connection()
    channel = connection.channel()
    channel.basic_publish(exchange=config.rabbitmq['exchange'],
                          routing_key='mail.command.delete',
                          body=json.dumps(content, indent=False, sort_keys=False))
    connection.close()
    logger.info('Email accepted. Delete request sent for %s' % content)


def post_diaspora(data):

    posted = False

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
            posted = True

            # delete saved image
            os.remove(image_filename)

    # post text
    else:
        stream.post(message)
        posted = True

    if posted:
        mail(data['from'], 'RE: ' + data['subject'], message)


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


def mail(to_email, subject, message):

    msg = {
        'to': to_email,
        'subject': subject,
        'content': message
    }
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    channel.basic_publish(exchange=config.rabbitmq['exchange'],
                          routing_key='mail.command.send',
                          body=json.dumps(msg, indent=False, sort_keys=False))
    connection.close()
    logger.debug('Email for %s posted' % to_email)


def process_message(chan, method, properties, body):
    topic = method.routing_key
    data = json.loads(body)

    if topic == 'mail.message' and data['subject'].upper() == 'DIASPORA':
        logger.info('new message => {}'.format(data))
        send_delete_command(data)
        post_diaspora(data)


class CommandConsumer(Thread):

    def run(self):

        connection = get_rabbitmq_connection()
        self.channel = connection.channel()
        self.channel.exchange_declare(exchange=config.rabbitmq['exchange'],
                                      exchange_type='topic')

        result = self.channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(exchange=config.rabbitmq['exchange'],
                                queue=queue_name,
                                routing_key='mail.message')
        self.channel.basic_consume(process_message,
                                   queue=queue_name,
                                   no_ack=True)
        self.channel.start_consuming()

    def stop_gracefully(self):
        self.channel.stop_consuming()


def start():
    consumer.start()


def stop():
    consumer.stop_gracefully()


consumer = CommandConsumer()
