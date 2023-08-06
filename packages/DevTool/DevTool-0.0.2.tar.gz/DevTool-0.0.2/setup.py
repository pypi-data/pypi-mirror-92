'''
@lanhuage: python
@Descripttion: 
@version: beta
@Author: xiaoshuyui
@Date: 2020-07-10 10:09:24
LastEditors: xiaoshuyui
LastEditTime: 2021-01-15 14:16:55
'''
from devtool import __version__, __appname__
import os
from setuptools import setup, find_packages
# import pypandoc


def open_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname),
                encoding='utf-8')


# long_description = pypandoc.convert_file(os.path.join(os.path.dirname(__file__), 'README.md'), 'rst')
# requestments = open_file('requirements.txt')

setup(
    name=__appname__,
    version=__version__,
    author='Chengxi GU',
    author_email='guchengxi1994@qq.com',
    packages=find_packages(),
    package_data={'': ['*.yaml']},
    long_description_content_type='text/markdown',
    url='https://github.com/guchengxi1994/dev-tool-for-python',
    license="MIT License",
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'setuptools==41.0.1', 'termcolor==1.1.0',
        'concurrent_log_handler==0.9.16', 'PyYAML==5.1.1'
    ],
    description='a small tool for python development',
    long_description=open_file('README.md').read(),
    zip_safe=True,
    entry_points={'console_scripts': ['devtool = devtool.main:script']},
)