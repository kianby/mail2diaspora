#!/usr/bin/env python
# -*- coding: utf-8 -*-


def cron(func):
    def wrapper():
        func()

    return wrapper
