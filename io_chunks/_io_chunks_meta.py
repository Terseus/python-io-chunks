# -*- coding: utf-8 -*-
"""TODO: doc module"""


NAME = "io-chunks"
VERSION = (1, 0, 1)
VERSION_STR = '.'.join(map(str, VERSION))
LICENSE = "MIT"
DESCRIPTION = "Stream chunks compatible with IO standard library"
AUTHOR = "David Caro"
AUTHOR_EMAIL = "terseus@gmail.com"
KEYWORDS = [
    "io",
    "library",
    "development",
    "chunk",
    "file",
    "read",
    "write",
    "stream"
]
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.2",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
URL = 'https://github.com/Terseus/python-io-chunks'
TESTS_REQUIRE = ["nose"]
PACKAGES_EXCLUDED = ["docs", "tests", "venv"]
INSTALL_REQUIRES = ["six"]
EXTRAS_REQUIRE = {
    'dev': [
        'flake8==3.5.0',
        'pytest>=3.6.2',
        'Sphinx>=1.7.5',
        'tox>=3.1.2',
    ],
}
