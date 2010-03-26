#!/usr/bin/env python
# -*- coding: utf-8 -*-

# webob imports
from webob import Request, Response
from webob import exc

# matplotlib imports
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

# controlsystems imports
from controlsystems.types import TransferFunction as tf
from controlsystems.pid_simulation import *
from controlsystems.discretization import *

# local imports
from models import models

# stdlib imports
import json
import os
import re
import sys
import StringIO


class Application(object):
    
    routes = [
        (r'^/$', 'index'),
        (r'^/model/([0-9]+)', 'model'),
        (r'^/plot/([0-9]+)', 'plot'),
    ]
    
    def __call__(self, environ, start_response):
        req = Request(environ)
        resp = None
        for regex, act in self.routes:
            match = re.match(regex, req.path_info)
            if match:
                try:
                    try:
                        meth = getattr(self, 'act_%s' % act)
                    except AttributeError:
                        raise exc.HTTPBadRequest('No such action: %r' % act).exception
                    resp = meth(req, list(match.groups()))
                except exc.HTTPException, e:
                    resp = e
        if resp is None:
            resp = exc.HTTPBadRequest('No route available').exception
        return resp(environ, start_response)

    def __additional_form(self, req, vars):
        model = models[vars[0]]
        aux = {}
        if model.additional_form is not None:
            for name in model.additional_form:
                if name in req.GET:
                    aux[name] = float(req.GET[name])
        return aux
    
    def __get_nmethod(self, req):
        m = req.GET['n_method']
        if m == '1':
            return Euler
        elif m == '2':
            return RungeKutta2
        elif m == '3':
            return RungeKutta3
        else:
            return RungeKutta4
    
    def __get_tmethod(self, req):
        m = req.GET['t_method']
        if m == '1':
            return ZieglerNichols
        elif m == '2':
            return CohenCoon
        elif m == '3':
            return ChienHronesReswick0
        else:
            return ChienHronesReswick20

    def act_index(self, req, vars):
        mydir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(mydir, 'html/index.html')) as fp:
            html = fp.read()
        return Response(html)

    def act_model(self, req, vars):
        model = models[vars[0]]
        aux = None
        if model.additional_form is not None:
            aux = '<table id="add_form">\n'
            for name in model.additional_form:
                aux += """\
<tr>
    <td><label for="%(name)s">%(name)s:</label></td>
    <td><input type="text" name="%(name)s" class="required number" /></td>
</tr>
""" % {'name': name}
            aux += '</table>'
        
        return Response(
            content_type = 'application/json',
            body = json.dumps({
                'model': {
                    'id': vars[0],
                    'img': model.get_model_img(),
                    'form': aux,
                }
            })
        )
    
    def act_plot(self, req, vars):
        
        nmethod = self.__get_nmethod(req)
        tmethod = self.__get_tmethod(req)
        
        args = self.__additional_form(req, vars)
        g = models[vars[0]].tf_callback(**args)
        
        sample = float(req.GET['Sample_Time'])
        time = float(req.GET['Total_Time'])
        what = int(req.GET['what'])
        
        fig = Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(
            111,
            xlabel = 'Tempo (seg)',
            ylabel = 'Amplitude',
        )
        
        t, y = nmethod(g, sample, time)
        ax.plot(t, y, label='Resposta ao Degrau')
        
        kp, ki, kd = tmethod(g, sample, time, nmethod)
        
        if what == 2:
            g_ = tf([kd, kp, ki], [1, 0])
            my_g = (g_ * g).feedback_unit()
            t1, y1 = nmethod(my_g, sample, time)
            ax.plot(t1, y1, label='Resposta ao Degrau Controlada')
        else:
            t1, y1 = tuning_rule(t, y)
            ax.plot(t1, y1, label='Reta de Carga')
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

        
        leg = ax.legend(
            loc = 'best',
            prop = {'size': 'x-small'},
            title = 'kp=%.1f; ki=%.1f; kd=%.1f;' % (kp, ki, kd),
        )

        canvas = FigureCanvas(fig)
        image = StringIO.StringIO()
        canvas.print_png(image)
        return Response(
            content_type = 'image/png',
            body = image.getvalue()
        )


application = Application()

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8080, application)
    print 'Serving on http://localhost:8080'
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print '^C'
