'''
lanhuage: python
Descripttion: 
version: beta
Author: xiaoshuyui
Date: 2021-01-06 08:34:53
LastEditors: xiaoshuyui
LastEditTime: 2021-01-08 16:52:58
'''

from devtool import infoDecorate, setWrap


@setWrap
def fc1_1():
    print(11)

@infoDecorate('test',name='123',age='12')
def fc1_2():
    print(12)

def fc1_3():
    print(13)

def fc1_4():
    print(14)