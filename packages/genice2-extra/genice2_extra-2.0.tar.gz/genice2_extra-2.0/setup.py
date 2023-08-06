#!/usr/bin/env python

# from distutils.core import setup, Extension
from setuptools import setup, Extension

long_desc = "".join(open("README.md").readlines())


setup(
    name='genice2_extra',
    version='2.0', # for genice2
    description='Installs all extra plugins for GenIce.',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
    ],
    author='Masakazu Matsumoto',
    author_email='vitroid@gmail.com',
    url='https://github.com/vitroid/genice-extra/',
    keywords=['genice'],
    install_requires=['genice2-cage',
                      'genice2-rdf',
                      'genice2-svg',
                      'genice2-cif',
                      'genice2-twist',
                      ],

    license='MIT',
)
