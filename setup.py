#!/usr/bin/env python
from setuptools import setup

setup(
    name='django-extraconfig',
    version='0.1',
    description=('An entry-point based solution to extend'
                 'the Django configuration.'),
    long_description=open('README.rst').read(),
    keywords='Django settings',
    author='Sever Banesiu',
    author_email='banesiu.sever@gmail.com',
    url='http://github.com/pbs/django-extraconfig/',
    license='BSD',
    py_modules=['extraconfig'],
)
