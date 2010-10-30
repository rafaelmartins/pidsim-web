# -*- coding: utf-8 -*-
"""
    blohg.views.main
    ~~~~~~~~~~~~~~~~
    
    View module that deals with the "static" pages generation.
    
    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

from flask import Module, render_template, make_response

main = Module(__name__)


@main.route('/')
def home():
    return render_template('index.html')


@main.route('/js')
def js():
    response = make_response(render_template('pidsim.js'))
    response.headers['Content-Type'] = 'text/javascript; charset=utf-8'
    return response
