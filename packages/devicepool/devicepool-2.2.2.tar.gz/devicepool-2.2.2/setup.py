#!/usr/bin/python
# -*- coding: UTF-8 -*-

import setuptools


def readme():
  with open('README.md', 'r') as f:
    return f.read()

setuptools.setup(
	
	name='devicepool',
    version='2.2.2',
    author='Ding Yi',
    author_email='dvdface@hotmail.com',
    url='https://github.com/dvdface/devicepool',
    description='the package used to manage resources in the resource pool.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    py_modules=['devicepool'],
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)