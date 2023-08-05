#!/usr/bin/env python

from setuptools import setup

setup(name='CB_ModernAPI',
      version='0.1',
      description='Module Wrapper for MordernMT API',
      author='Leynaïc Brisse',
      author_email='leynaic.brisse@gmail.com',
      packages=['cb_wrapper'],
      install_requires=[
          'pytest', 'pyyaml', 'requests'
      ]
      )
