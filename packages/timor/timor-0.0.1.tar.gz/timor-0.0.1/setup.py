# coding=utf-8
from setuptools import setup

setup(
    name='timor',
    version='0.0.1',
    author='puke',
    author_email='1129090915@qq.com',
    url='https://github.com/puke3615',
    description=u'Just a test',
    packages=['timor'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'tma=timor:tma',
            'tmb=timor:tmb'
        ]
    }
)