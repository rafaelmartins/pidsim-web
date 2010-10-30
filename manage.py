#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    blohg.script
    ~~~~~~~~~~~~
    
    Module with the CLI script related stuff.
    
    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

from flaskext.script import Server, Manager
from pidsim_web import create_app


def create_script():
    """Script object factory
    
    :param config_file: the configuration file path.
    :return: the script object (Flask-Themes' Manager instance).
    """
    
    app = create_app()
    script = Manager(app)
    return script


if __name__ == '__main__':
    create_script().run()
