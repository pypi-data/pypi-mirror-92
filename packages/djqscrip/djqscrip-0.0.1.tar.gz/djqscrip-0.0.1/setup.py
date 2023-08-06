# -*- encoding: utf-8 -*-
'''
@File    :   setup.py
@Time    :   2021/01/20 17:02:56
@Author  :   Jiaqi Duan
@Version :   0.0.1
'''

# here put the import lib
from setuptools import setup, find_packages


setup(
    name="djqscrip",
    version="0.0.1",
    license="MIT Licence",
 
    url="https://github.com/duanjiaqi/djqscrips",
    author="djq",
 
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[],
    entry_points = {
        'console_scripts': [
            'cv_resize_img = djqscrips.python:cv_resize_img',
        ]
    }
)