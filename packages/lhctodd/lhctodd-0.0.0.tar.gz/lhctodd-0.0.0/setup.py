#!/usr/bin/env python
# Copyright (c) 2021, Yacine Haddad
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/yhaddad/lhctodd for details.

from setuptools import setup
from os import path

basedir = path.abspath(path.dirname(__file__))
with open(path.join(basedir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    long_description=long_description,
    long_description_content_type='text/markdown',
)
