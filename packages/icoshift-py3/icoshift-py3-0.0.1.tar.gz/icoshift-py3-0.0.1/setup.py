#!/usr/bin/env python
# coding=utf-8
import sys
from copy import copy
#import distribute_setup
#distribute_setup.use_setuptools()

import setuptools

setuptools.setup(
    name="icoshift-py3",
    version="0.0.1",
    author="Ryan Guild",
    author_email="rdg27@pitt.edu",
    description="Spectral Icoshift updated for python v.3",
    url="https://github.com/Sour-Smelno/icoshift.git",
   
    python_requires='>=3.0',


    packages=['icoshift-py3'],
    include_package_data=True,
    package_data={
        '': ['*.txt', '*.rst', '*.md'],
    },
    exclude_package_data={'': ['README.txt']},

    install_requires=[
            'numpy>=1.7.1',
            'scipy>=0.12.0',
            ],

    keywords='bioinformatics metabolomics research analysis science',
    license='GPL',
    classifiers=['Development Status :: 4 - Beta',
               'Natural Language :: English',
               'Operating System :: OS Independent',
               'Programming Language :: Python :: 2',
               'License :: OSI Approved :: BSD License',
               'Topic :: Scientific/Engineering :: Bio-Informatics',
               'Intended Audience :: Science/Research',
               'Intended Audience :: Education',
              ],

    )
