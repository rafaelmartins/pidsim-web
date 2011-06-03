#!/usr/bin/env python
# -*- coding: utf-8 -*-

from babel.messages import frontend as babel
from setuptools import setup

import pidsim.web as pidsim_web

setup(
    name = 'pidsim.web',
    version = pidsim_web.__version__,
    license = pidsim_web.__license__,
    description = pidsim_web.__description__,
    long_description = open('README.rst').read(),
    author = pidsim_web.__author__,
    author_email = pidsim_web.__email__,
    url = pidsim_web.__url__,
    platforms = 'any',
    packages = [
        'pidsim.web',
    ],
    namespace_packages = ['pidsim'],
    scripts = ['pidsim-web'],
    zip_safe = False,
    include_package_data = True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Education',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    cmdclass = {
        'compile_catalog': babel.compile_catalog,
        'extract_messages': babel.extract_messages,
        'init_catalog': babel.init_catalog,
        'update_catalog': babel.update_catalog,
    }
)
