# -*- coding: utf-8 -*-
"""setup.py."""
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as fd:
    long_description = fd.read()


INSTALL_REQUIRES = [
]
VERSION = '0.0.3'

setup(
    name='onelibs',
    version=VERSION,
    description='onelibs is an out-of-the-box libs written in python',
    long_description=long_description,
    author='codingcat',
    author_email='istommao@gmail.com',
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
    package_dir={'onelibs': 'onelibs'},
    include_package_data=True,
    zip_safe=False,
    url='https://github.com/istommao/onelibs-python',
    keywords='onelibs',
    entry_points="""
    [console_scripts]
    onelibs=onelibs.scripts:main
    """
)
