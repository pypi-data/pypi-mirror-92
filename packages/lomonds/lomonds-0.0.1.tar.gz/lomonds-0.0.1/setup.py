#!/usr/bin/env python

from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Programming Language :: Python',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    # 'Programming Language :: Python :: 3.8',
    'Topic :: Internet'
]

# http://bit.ly/2alyerp

with open('README.md') as f:
    long_desc = f.read()

setup(
    name='lomonds',
    version="0.0.1",
    description="Websocket Client Library",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    author='iessen',
    author_email='essen.wang.sh@gmail.com',
    url='https://github.com/iessen/dataplicity-lomond',
    platforms=['any'],
    packages=find_packages(),
    classifiers=classifiers,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    install_requires=[
        'six>=1.10.0',
    ],
    zip_safe=True
)
