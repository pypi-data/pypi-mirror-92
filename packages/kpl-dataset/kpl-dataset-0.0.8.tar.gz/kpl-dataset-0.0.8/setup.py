#!/usr/bin/env python
from setuptools import setup, find_packages


setup(name='kpl-dataset',
      version='0.0.8',
      platforms='any',
      description='KPL Dataset',
      packages=find_packages(),
      install_requires=[
          'protobuf==3.11.0'
      ],
      classifiers=[
          'Programming Language :: Python',
          'Operating System :: OS Independent',
      ])
