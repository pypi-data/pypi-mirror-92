'''
lanhuage: python
Descripttion: 
version: beta
Author: xiaoshuyui
Date: 2021-01-26 08:53:04
LastEditors: xiaoshuyui
LastEditTime: 2021-01-26 10:24:01
'''
__is_pyquery_installed__ = False

from devtool.utils.devtool_exceptions import ModuleNotInstallelException
import re

try:
    from pyquery import PyQuery
    __is_pyquery_installed__ = True
except:
    pass

python_module_url = {
    'pypi': 'https://pypi.org/simple/',
    'tshua': 'https://pypi.tuna.tsinghua.edu.cn/simple/',
    'ali': "http://mirrors.aliyun.com/pypi/simple/"
}

reg = "\d+\.\d+(\.\d+)*"


def search_module_isExist(moduleName: str, searchEngine: str = 'pypi') -> list:
    global python_module_url
    try:
        s = PyQuery(
            python_module_url.get(searchEngine, python_module_url['pypi']) +
            '{}/'.format(moduleName))
        # print(s)
        validVersion = s.find('body').find('a')
        # print(type(validVersion))
        if validVersion is not None:
            # print(x)
            return [i.text() for i in validVersion.items('a')]
        else:
            return None
    except:
        return None


def searchScript(names: list):
    global reg
    if __is_pyquery_installed__:
        for tmp in names:
            vs = search_module_isExist(tmp)
            if vs is not None:
                v = re.search(reg, vs[-1]).group()
                print('module {} lastest version is {}'.format(tmp, v))
            else:
                print('module {} is not found'.format(tmp))
    else:
        raise ModuleNotInstallelException(
            '{} not installed.'.format('pyquery'))
