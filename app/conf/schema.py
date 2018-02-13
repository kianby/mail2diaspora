#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with https://app.quicktype.io
#   name: mail2diaspora

json_schema = """
{
    "$ref": "#/definitions/Mail2Diaspora",
    "definitions": {
        "General": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "tempdir": {
                    "type": "string"
                }
            },
            "required": [
                "tempdir"
            ],
            "title": "general"
        },
        "Rabbitmq": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "active": {
                    "type": "boolean"
                },
                "host": {
                    "type": "string"
                },
                "port": {
                    "type": "integer"
                },
                "username": {
                    "type": "string"
                },
                "password": {
                    "type": "string"
                },
                "vhost": {
                    "type": "string"
                },
                "exchange": {
                    "type": "string"
                }
            },
            "required": [
                "active",
                "exchange",
                "host",
                "password",
                "port",
                "username",
                "vhost"
            ],
            "title": "rabbitmq"
        },
        "Diaspora": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "pod": {
                    "type": "string"
                },
                "username": {
                    "type": "string"
                },
                "password": {
                    "type": "string"
                }
            },
            "required": [
                "password",
                "pod",
                "username"
            ],
            "title": "diaspora"
        },
        "Mail2Diaspora": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "general": {
                    "$ref": "#/definitions/General"
                },
                "rabbitmq": {
                    "$ref": "#/definitions/Rabbitmq"
                },
                "diaspora": {
                    "$ref": "#/definitions/Diaspora"
                }
            },
            "required": [
                "diaspora",
                "general",
                "rabbitmq"
            ],
            "title": "mail2diaspora"
        }
    }
}
"""