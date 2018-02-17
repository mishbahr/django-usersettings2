#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import codecs
import usersettings

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = usersettings.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = codecs.open('README.rst').read()
history = codecs.open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-usersettings2',
    version=version,
    description="""The missing extension to the Django “sites” framework, use it to store additional information for your Django-powered sites.""",
    long_description=readme + '\n\n' + history,
    author='Mishbah Razzaque',
    author_email='mishbahx@gmail.com',
    url='https://github.com/mishbahr/django-usersettings2',
    packages=[
        'usersettings',
    ],
    include_package_data=True,
    install_requires=[
        'django>=1.5.1',
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-usersettings2',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
