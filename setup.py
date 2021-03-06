# -*- coding: utf-8 -*-


from setuptools import setup, find_packages
from codecs import open
from os import path
import sys


HERE = path.abspath(path.dirname(__file__))
sys.path.append(path.join(HERE, 'io_chunks'))


import _io_chunks_meta as app_meta  # noqa


# Get the long description from the README file
def get_long_description():
    with open(path.join(HERE, 'README.rst'), encoding='utf-8') as f:
        return f.read()


setup(
    name=app_meta.NAME,
    version=app_meta.VERSION_STR,
    author=app_meta.AUTHOR,
    author_email=app_meta.AUTHOR_EMAIL,
    license=app_meta.LICENSE,
    description=app_meta.DESCRIPTION,
    long_description=get_long_description(),
    classifiers=app_meta.CLASSIFIERS,
    keywords=app_meta.KEYWORDS,
    packages=find_packages(exclude=['docs', 'tests', 'venv']),
    url=app_meta.URL,
    install_requires=[
        'six'
    ],
    extras_require={
        'dev': [
            'flake8==3.5.0',
            'pytest>=3.6.2',
            'Sphinx>=1.7.5',
            'tox>=3.1.2',
        ],
    },
)
