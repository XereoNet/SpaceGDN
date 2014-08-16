import os
import sys

from setuptools import setup, find_packages
from distutils.sysconfig import get_python_lib

setup(
    name='SpaceGDN',
    version='2.0.0-dev',
    url='https://github.com/connor4312/querytree',
    author='Connor Peet',
    author_email='connor@connorpeet.com',
    description='Game Delivery Network for SpaceCP',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['Flask',
                      'Flask-Script',
                      'uwsgi',
                      'requests',
                      'beautifulsoup4',
                      'lxml',
                      'raven[flask]',
                      'pymongo']
)