# Copyright 2017 Brandon Schlueter

from setuptools import setup, find_packages

setup(
    name='yas',
    summary='Yet Another Slack bot',
    version='2.0-rc1',
    packages=find_packages(),
    install_requires=[
        'slackclient==1.0.5',
        'websocket-client==0.40.0'
    ],
    entry_points={
        'console_scripts': [
            'yas = yas.core.application:run'
        ]
    },
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python",
    ]
)
