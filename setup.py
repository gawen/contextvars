#!/usr/bin/env python

try:
    from setuptools import setup

except:
    from distutils.core import setup

import contextvars

setup(
    name = "contextvars",
    description = "Contexted variables framework for Python",
    
    py_modules = ["contextvars"],
    #test_suite = "tests",

    version = contextvars.__version__,
    author = contextvars.__author__,
    author_email = contextvars.__email__,
    url = "https://github.com/gawen/contextvars",
    license = contextvars.__license__,
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
)
