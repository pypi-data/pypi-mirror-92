#!/usr/bin/env python

# from distutils.core import setup, Extension
from setuptools import setup, Extension, find_packages
import os
import codecs
import re

#Copied from wheel package
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(os.path.dirname(__file__), 'genice2_twist', '__init__.py'),
                 encoding='utf8') as version_file:
    metadata = dict(re.findall(r"""__([a-z]+)__ = "([^"]+)""", version_file.read()))

long_desc = "".join(open("README.md").readlines())


setup(
    name='genice2_twist',
    version=metadata['version'],
    description='Twist analysis plugin for GenIce.',
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
    url='https://github.com/vitroid/genice-twist/',
    keywords=['genice', 'chirality'],

    packages=find_packages(),

    entry_points = {
        'genice2_format': [
            'twist  = genice2_twist.formats.twist',
        ],
    },
    install_requires=['genice2', 'genice2-svg>=0.7', 'twist-op>=0.2', 'sklearn'],

    license='MIT',
)
