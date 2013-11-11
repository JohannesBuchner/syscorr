#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except:
    from distutils.core import setup

long_description = None
with open('README.rst') as file:
    long_description = file.read()

setup(
    name = "syscorr",
    version = "0.1",
    description = "Bayesian correlation swiss army knife",
    author = "Johannes Buchner",
    author_email = "johannes.buchner.acad [@t] gmx.com",
    maintainer = "Johannes Buchner",
    maintainer_email = "johannes.buchner.acad [@t] gmx.com",
    url = "http://johannesbuchner.github.com/syscorr/",
    license = "AGPLv3",
    packages = ["syscorr"],
    provides = ["syscorr"],
    requires = ["numpy (>=1.5)", "matplotlib", "scipy", "uncertainties", "jbopt", "pymultinest"],
    long_description=long_description,
)

