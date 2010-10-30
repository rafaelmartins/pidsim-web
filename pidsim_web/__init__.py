# -*- coding: utf-8 -*-
"""
    pidsim_web
    ~~~~~~~~~~
    
    Main package.
    
    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

from flask import Flask, render_template
from flaskext.babel import Babel

from pidsim_models import models

from pidsim_web.views.main import main

def create_app():
    """Application factory.
    
    :param config_file: the configuration file path.
    :return: the WSGI application (Flask instance).
    """
    
    # create the app object
    app = Flask(__name__)
    
    # register some sane default config values
    app.config.setdefault('DEBUG', False)
    app.config.setdefault('SECRET_KEY', 'development key')
    
    # load configs
    app.config.from_envvar('PIDSIM_SETTINGS', True)
    
    # setup extensions
    babel = Babel(app)
    
    @app.context_processor
    def setup_jinja2():
        return dict(
            models = models.index,
        )

    @babel.localeselector
    def get_locale():
        # we just have pt_BR for now
        return 'pt_BR'
    
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404
    
    app.register_module(main)
    
    return app
