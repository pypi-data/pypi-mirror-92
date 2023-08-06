#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- file: setup.py -*-
# -*- purpose: -*-

'''
setup.py file for fisbar module
'''

import setuptools

PROJ_NAME = open('projname.txt', 'r').read()
PROJ_VERSION = open('version.txt', 'r').read()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name=PROJ_NAME,
      version=PROJ_VERSION,
      packages=['fisbar'],
      description='Python implementation of BARFIT routine by A Sierk',
      long_description=long_description,
      long_description_content_type="text/markdown", 
      author='Greg Henning',
      author_email='ghenning@iphc.cnrs.fr',
      url='https://gitlab.in2p3.fr/gregoire.henning/fisbar-python',
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)",
        "Operating System :: OS Independent",
        ],
      python_requires='>=3.6',
      install_requires=[
          'numpy',
      ],
      )
