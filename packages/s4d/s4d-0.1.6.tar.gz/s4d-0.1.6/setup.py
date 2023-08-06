#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from distutils.core import setup

# patch distutils if it can't cope with the "classifiers" or
# "download_url" keywords
from sys import version
if version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None

def get_s4d_version():
    with open('s4d/__init__.py') as f:
        s = [l.rstrip() for l in f.readlines()]
        version = None
        for l in s:
            if '__version__' in l:
                version = l.split('=')[-1]
        if version is None:
            raise RuntimeError('Can not detect version from s4d/__init__.py')
        return eval(version)

setup(
    name='s4d',
    version=get_s4d_version(),
    author='Sylvain MEIGNIER',
    author_email='s4d@univ-lemans.fr',
    packages=['s4d', 's4d.alien', 's4d.clustering', 's4d.gui', 's4d.nnet'],
    url='https://projets-lium.univ-lemans.fr/s4d/',
    download_url='http://pypi.python.org/pypi/s4d/',
    license='LGPL',
    platforms=['Linux, Windows', 'MacOS'],
    description='S4D: SIDEKIT for Diarization',
    long_description=open('README.txt').read(),
    install_requires=[
        "numpy==1.19.0",
        "pyparsing >= 2.4.7",
        "python-dateutil >= 2.8.1",
        "scipy>=1.6.0",
        "six>=1.15.0",
        "matplotlib>=3.3.2",
        "pyroomacoustics==0.4.2",
        "soundfile>= 0.10.3",
        "torch >= 1.7.1",
        "torchvision>=0.8.2",
        "tqdm>=4.55.1",
        "pyyaml>=5.4.1",
        "h5py>=2.10.0",
        "pandas>=1.2.1",
        "scikit-learn>=0.24.1",
        "bottleneck>=1.3.1",
        "setuptools>=38.5.2",
        "sidekit>=1.3.7",
        "sortedcontainers>=1.5.9"
    ],
    package_data={'s4d': ['docs/*']},
    classifiers=[        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Scientific/Engineering",
        ]
)


