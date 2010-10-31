# -*- coding: utf-8 -*-
"""
    pidsim_web
    ~~~~~~~~~~
    
    Main package.
    
    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

from flask import Flask, render_template, make_response, jsonify, request
from flaskext.babel import Babel, get_locale, _

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from pidsim.approximation import methods as pade
from pidsim.discretization import *
from pidsim.pid_simulation import *
from pidsim.types import tf

from pidsim_models import models

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from urllib import pathname2url


# create the app object
app = Flask(__name__)

# register some sane default config values
app.config.setdefault('DEBUG', False)
app.config.setdefault('SECRET_KEY', 'development key')
app.config.setdefault('MIMETEX_URL', 'http://pidsim.rafaelmartins.eng.br/cgi-bin/mimetex.cgi')

# load configs
app.config.from_envvar('PIDSIM_SETTINGS', True)

# setup extensions
babel = Babel(app)

@app.context_processor
def setup_jinja2():
    return dict(
        models = models.index,
        pade_orders = pade.keys(),
    )

@babel.localeselector
def get_locale():
    # we just have pt_BR for now
    return 'en_US'


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/pidsim.js')
def js():
    response = make_response(render_template('pidsim.js'))
    response.headers['Content-Type'] = 'text/javascript; charset=utf-8'
    return response

@app.route('/model/<int:id>')
def model(id):
    model = models.index[id](str(get_locale()))
    img_url = app.config['MIMETEX_URL'] + '?' + \
        pathname2url('\\fs5 ' + model.transfer_function)
    form = None
    if len(model.args) > 0:
        form = render_template('additional_form.html', form = model.args)
    return jsonify(
        name = model.get('name'),
        description = model.get('description'),
        img = img_url,
        form = form
    )

@app.route('/plot/<int:id>')
def plot(id):
    
    # get the discretization method
    _nmethod = request.args['n_method']
    if _nmethod == '1':
        nmethod = Euler
    elif _nmethod == '2':
        nmethod = RungeKutta2
    elif _nmethod == '3':
        nmethod = RungeKutta3
    else:
        nmethod = RungeKutta4
    
    # get the pid_simulation method
    _tmethod = request.args['t_method']
    if _tmethod == '0':
        tmethod = None
    elif _tmethod == '1':
        tmethod = ZieglerNichols
    elif _tmethod == '2':
        tmethod = CohenCoon
    elif _tmethod == '3':
        tmethod = ChienHronesReswick0
    else:
        tmethod = ChienHronesReswick20
    
    # get process parameters
    parameters = {}
    model = models.index[id](str(get_locale()))
    if model.args is not None:
        for arg in model.args:
            if arg in request.args:
                parameters[arg] = float(request.args[arg])
    
    # get transfer function
    g = model.callback(**parameters)
    
    # get options
    sample = float(request.args.get('Sample_Time', 0.01))
    time = float(request.args.get('Total_Time', 10))
    what = int(request.args.get('what', 1))
    
    # create the figure
    fig = Figure(figsize=(8, 6), dpi=100)
    ax = fig.add_subplot(
        111,
        xlabel = _('Tempo (seg)'),
        ylabel = _('Amplitude'),
    )
    
    # discretize the transfer function and plot it
    t, y = nmethod(g, sample, time)
    ax.plot(t, y, label=_('Resposta ao Degrau'))
    
    # simulate the PID controller, if wanted
    if tmethod is not None:
        kp, ki, kd = tmethod(g, sample, time, nmethod)
    else:
        try:
            kp = float(request.args.get('kp', 0))
        except:
            kp = 0
        
        try:
            ki = float(request.args.get('ki', 0))
        except:
            ki = 0
        
        try:
            kd = float(request.args.get('kd', 0))
        except:
            kd = 0
    
    # plot the simulated controller
    if what == 2:
        
        # transfer function of the PID controller
        g_ = tf([kd, kp, ki], [1, 0])
        my_g = (g_ * g).feedback_unit()
        
        # discretize the controlled system
        t1, y1 = nmethod(my_g, sample, time)
        ax.plot(t1, y1, label=_('Resposta ao Degrau Controlada'))
    
    else:
        
        # generate the tuning_rule
        t1, y1 = tuning_rule(t, y)
        ax.plot(t1, y1, label=_('Reta de Sintonia'))
        ax.annotate(
            '28%', xy=(t1[1], y1[1]), xycoords='data',
            xytext=(t1[1]+(time/15.0), y1[1]),
            arrowprops=dict(facecolor='black', shrink=0.05),
        )
        ax.annotate(
            '63%', xy=(t1[2], y1[2]), xycoords='data',
            xytext=(t1[2]+(time/15.0), y1[2]),
            arrowprops=dict(facecolor='black', shrink=0.05),
        )

    # add the legend
    leg = ax.legend(
        loc = 'best',
        prop = {'size': 'x-small'},
        title = 'kp=%.1f; ki=%.1f; kd=%.1f;' % (kp, ki, kd),
    )
    
    # add the grid
    ax.grid(True)
    
    # generate a PNG file with the graph
    canvas = FigureCanvas(fig)
    image = StringIO()
    canvas.print_png(image)
    
    # return the generated image
    response = make_response(image.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response
