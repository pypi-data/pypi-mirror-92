#-*- coding:utf-8 -*-
# @Author  : lx

from setuptools import setup, find_packages


setup(
    name = 'lxpy',
    version = '1.2.6',
    author = 'ying5338619',
    author_email = '125066648@qq.com',
    install_requires=['lxml'],
    packages=find_packages(),
    url='https://github.com/lixi5338619/lxpy.git',
    description = 'Web crawler and data processing toolkit !',
    long_description = open('readme.md','r',encoding='utf-8').read(),
)
