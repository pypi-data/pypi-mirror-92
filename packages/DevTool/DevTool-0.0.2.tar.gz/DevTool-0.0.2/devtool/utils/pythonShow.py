'''
lanhuage: python
Descripttion: 
version: beta
Author: xiaoshuyui
Date: 2021-01-26 08:52:50
LastEditors: xiaoshuyui
LastEditTime: 2021-01-26 10:34:43
'''
from devtool.utils.devtool_exceptions import ModuleNotInstallelException
import importlib
import difflib

__is_smoothnlp_installed__ = False
try:
    import smoothnlp
    __is_smoothnlp_installed__ = True
except:
    pass


def showScript(name: str):
    tmp = name.split('.')
    moduleName = tmp[0]
    try:
        module = importlib.__import__(moduleName)
    except:
        print('module not found \n try search {}'.format(moduleName))
        return

    tmp.remove(tmp[0])
    methodList = dir(module)
    if __is_smoothnlp_installed__:
        if len(tmp) > 0:
            methodName = '.'.join(tmp)
            if methodName in methodList:
                impo = getattr(module, methodName)
                words = impo.__doc__
                tmp = smoothnlp.split2sentences(str(words))
                print(tmp[0])
                return
            else:
                print('module {} not contain {}'.format(
                    moduleName, methodName))
                lis = difflib.get_close_matches(methodName, methodList)
                if len(lis) > 0:
                    print('do you mean: {} ?'.format(' OR '.join(lis)))
                del lis
                return
        else:
            words = module.__doc__
            tmp = smoothnlp.split2sentences(str(words))
            print(tmp[0])
            del words, tmp
            return
    else:
        raise ModuleNotInstallelException(
            '{} not installed.'.format('smoothnlp'))
