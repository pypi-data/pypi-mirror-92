#! /usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools

setuptools.setup(
    name='restsql',
    version='2.0.0',
    description=(
        'RestSQL库。用json与数据库交互。'
    ),
    url='https://git.code.oa.com/tencent_cloud_mobile_tools/RestSQL',
    long_description='restsql',
    author="venzozhang",
    author_email='venzozhang@tencent.com',
    maintainer='oliverdding',
    maintainer_email='oliverdding@tencent.com',
    license='MIT License',
    packages=['restsql'],
    install_requires=[
        'numpy==1.16.6',
        'pandas==0.24.2',
        'pyyaml==5.4.1',
        'elasticsearch==6.8.1',
        'psycopg2-binary==2.8.6',
        'mysqlclient==1.4.6',
        'impyla==0.16.3'
    ],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
