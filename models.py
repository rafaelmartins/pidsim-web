# -*- coding: utf-8 -*-

from controlsystems.types import TransferFunction as tf
from controlsystems.types import Polynomial as pol

import urllib

class Model(object):
    
    def __init__(self, latex_model, tf_callback, additional_form=None):
        self.latex_model = latex_model
        self.tf_callback = tf_callback
        self.additional_form = additional_form
    
    def get_model_img(self):
        mimetex = 'http://rafaelmartins.webfactional.com/tex/mimetex.cgi'
        return mimetex + '?' + urllib.pathname2url('\\fs5 ' + self.latex_model)

def p5(n):
    print 'aaaa'
    a = pol([1, 1])
    for i in range(1, int(n)):
        a = a * pol([1, 1])
    return tf([1], list(a))

models = {
    '1': Model(
        'G_p(s) = \\frac{k}{(1+\\tau s)}',
        lambda k, Tau: tf([k], [Tau, 1]),
        ['k', 'Tau'],
    ),
    '2': Model(
        'G_p(s) = \\frac{k}{(1+T_1 s)(1+T_2 s)}',
        lambda k, T1, T2: tf([k], pol([T1, 1]) * pol([T2, 1])),
        ['k', 'T1', 'T2'],
    ),
    '3': Model(
        'G_p(s) = \\frac{k(1-T_1 s)}{(1+T_1 s)(1+T_2 s)}',
        lambda k, T1, T2: tf([-T1*k, k], pol([T1, 1]) * pol([T2, 1])),
        ['k', 'T1', 'T2'],
    ),
    '4': Model(
        'G_p(s) = \\frac{k(1+T_4 s)}{(1+T_1 s)(1+T_2 s)(1+T_3 s)} e^{-T_t s}',
        lambda k, T1, T2, T3, T4, Tt: tf([], []),
        ['k', 'T1', 'T2', 'T3', 'T4', 'Tt'],
    ),
    '5': Model(
        'G_p(s) = \\frac{1}{(s+1)^n}',
        p5,
        ['n'],
    ),
    '6': Model(
        'G_p(s) = \\frac{1}{(s+1)(\\alpha s+1)(\\alpha ^2 s+1)(\\alpha ^3 s+1)}',
        lambda Alpha: tf([1], (pol([1, 1]) * pol([Alpha, 1])) * (pol([Alpha*Alpha, 1]) * pol([Alpha*Alpha*Alpha, 1]))),
        ['Alpha'],
    ),
    '7': Model(
        'G_p(s) = \\frac{1-\\alpha s}{(s+1)^3}',
        lambda Alpha: tf([-Alpha, 1], (pol([1, 1]) * pol([1, 1])) * pol([1, 1])),
        ['Alpha'],
    ),
    '8': Model(
        'G_p(s) = \\frac{1}{(\\tau s +1)}e^{-s}',
        lambda tau: tf([], []),
        ['Tau'],
    ),
    '9': Model(
        'G_p(s) = \\frac{1}{(\\tau s +1)^2}e^{-s}',
        lambda tau: tf([], []),
        ['Tau'],
    ),
    '10': Model(
        'G_p(s) = \\frac{100}{(s+10)^2}\\left ( \\frac{1}{s+1} + \\frac{0,5}{s+0,05} \\right )',
        lambda: tf([100], pol([1, 10]) * pol([1, 10])) * (tf([1], [1, 1]) + tf([0.5], [1, 0.05])),
        None,
    ),
    '11': Model(
        'G_p(s) = \\frac{(s+6)^2}{s(s+1)^2 (s+36)}',
        lambda: tf(pol([1, 6]) * pol([1, 6]), (pol([1, 0]) * pol([1, 1])) * (pol([1, 1]) * pol([1, 36]))),
        None,
    ),
    '12': Model(
        'G_p(s) = \\frac{\\omega _0^2}{(s+1)(s^2+2\\zeta \\omega _0 s+\\omega _0^2)}',
        lambda Omega, Zeta: tf([Omega * Omega], pol([1, 1]) * pol([1, 2 * Zeta * Omega, Omega * Omega])),
        ['Omega', 'Zeta'],
    ),
    '13': Model(
        'G_p(s) = \\frac{1}{s^2 - 1}',
        lambda: tf([1], [1, 0, -1]),
        None,
    ),
    '14': Model(
        'G_p(s) = \\frac{1}{s(\\tau s + 1)}e^{-s}',
        lambda tau: tf([], []),
        ['Tau'],
    ),
}
