# -*- coding: utf-8 -*-
"""setup.py."""
from setuptools import setup, find_packages

INSTALL_REQUIRES = [
]
VERSION = '0.0.2'

setup(
    name='onelibs',
    version=VERSION,
    description='onelibs is an out-of-the-box libs written in python',
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
