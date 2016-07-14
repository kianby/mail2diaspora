#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from clize import clize, run


@clize
def bootstrap(config_pathname):

    os.environ['CONFIG_PATHNAME'] = config_pathname
    from mail2diaspora import app

if __name__ == '__main__':
    run(bootstrap)
