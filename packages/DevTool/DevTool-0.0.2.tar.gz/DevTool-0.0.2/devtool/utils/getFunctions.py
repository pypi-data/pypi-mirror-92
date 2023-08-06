'''
lanhuage: python
Descripttion: 
version: beta
Author: xiaoshuyui
Date: 2021-01-06 15:15:44
LastEditors: xiaoshuyui
LastEditTime: 2021-01-06 16:48:37
'''
from devtool import FuncAndName
import importlib
import inspect


def find_functions(modulelist: list, moduleName: str):
    res = []
    for i in modulelist:
        try:
            # print('===============>'+moduleName+'.'+i)
            submodulename = moduleName + '.' + i
            module = importlib.import_module(submodulename)
            # print(module)
            member_list = inspect.getmembers(module,
                                             predicate=inspect.isfunction)
            for funcname, func in member_list:
                if func.__module__.startswith(moduleName):
                    res.append(FuncAndName(funcname,func))
        except Exception as e:
            print(e)
    return list(set(res))