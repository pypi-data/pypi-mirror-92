'''
lanhuage: python
Descripttion: 
version: beta
Author: xiaoshuyui
Date: 2021-01-06 08:26:44
LastEditors: xiaoshuyui
LastEditTime: 2021-01-26 13:29:49
'''
import datetime
import importlib
import os

import yaml
from termcolor import colored

from devtool import (__current_platform__, do_nothing, infoDecorate, logit,
                     logit_logger, setWrap)
from devtool.utils.common import (match_datetime, validate_date,
                                  validate_datetime)
from devtool.utils.getFunctions import find_functions
from devtool.utils.getModules import find_modules
from devtool.utils.pythonSearch import searchScript
from devtool.utils.pythonShow import showScript

BASE_DIR = os.path.abspath(os.curdir)
LOG_PATH = BASE_DIR + os.sep + "DevLog" + os.sep + 'devlog.log'

abs_file = __file__
p, _ = os.path.split(abs_file)
yamlFilePath = p + os.sep + 'style.yaml'


class DevTool:
    storage = []
    currentModulePath = ''
    currentModuleName = ''

    @classmethod
    @logit()
    def exec(cls, moduleName=''):
        print('<================ Init... ================>')
        module = importlib.__import__(moduleName)
        modulePath = os.path.dirname(module.__file__)
        sub_modules = find_modules(modulePath)
        member_list = find_functions(sub_modules, moduleName)
        for i in member_list:
            try:
                i.func.__call__()
                if len(i.func.__annotations__) > 0:
                    # print(True)
                    val = map(lambda x: str(x),
                              list(i.func.__annotations__.values()))
                    # print(val)
                    i.info = ','.join(val)
                    # print(i.info)
                    cls.storage.append(i)
                # if i.func.__annotations__.get('wrapped_cached', False):
                #     cls.storage.append(i)
            except:
                continue
        print('<================ finish ================>')
        cls.currentModulePath = modulePath
        cls.currentModuleName = moduleName
        # print(cls.storage)
        return cls.storage

    @classmethod
    def grep(cls, moduleName: str, grepType, *kwds):
        """
        grepType should be a str in ['and','or'];
        moduleName can be 'this' ,which stands for cls.currentModuleName
        """
        if len(cls.storage) == 0:
            print(
                'Nothing found. Plz run DevTool.exec() first or just there is nothing to find.'
            )
            return
        else:
            if moduleName != 'this':
                thisStorage = cls.exec(moduleName)
            else:
                thisStorage = cls.storage
            if grepType not in ['and', 'or']:
                print(
                    "grepType should be a str in ['and','or'],  but got {}, use 'or' instead."
                    .format(grepType))
                grepType = 'or'

            remainedRes = []
            if grepType == 'or':
                for i in thisStorage:
                    for j in kwds:
                        if j in i.info:
                            remainedRes.append(i)

            if grepType == 'and':
                for i in thisStorage:
                    for j in kwds:
                        if not j in i.info:
                            break
                        remainedRes.append(i)
            cls.storage = remainedRes
            return remainedRes

    @classmethod
    def tree(cls, moduleName):
        if cls.currentModulePath == '':
            module = importlib.__import__(moduleName)
            modulePath = os.path.dirname(module.__file__)
        else:
            modulePath = cls.currentModulePath

        for root, _, files in os.walk(modulePath):
            level = root.replace(modulePath, '').count(os.sep)
            dir_indent = "|   " * (level - 1) + "|-- "
            file_indent = "|   " * level + "|-- "
            if not level:
                print('.')
            else:
                tmp = os.path.basename(root)
                if tmp != '__pycache__':
                    print('{}{}'.format(dir_indent, os.path.basename(root)))
                del tmp
            for f in files:
                # tmp = root + os.sep + f
                if not f.endswith('.pyc'):
                    print('{}{}'.format(file_indent, f))

    @staticmethod
    def logFilter(*kwds, **params):
        """
        kwds are the filters, can be like "ERROR" or function name. Also ,add '-' before kwds means except kwds. eg. '-ERROR' means 'NOT ERROR'
        
        params can be like "since='2021-01-08'","until='2021-01-09'", and specific log path "path='xx/xx/xx.log'"
        """
        path = params.get('path', None)
        if path is None:
            path = LOG_PATH
        if not os.path.exists(path):
            print('No Log File Found!')
            return
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            res = []
            # print(len(lines))
            for i in range(0, len(lines)):
                # if validate_datetime(i)
                loggedTime = match_datetime(lines[i])
                for j in kwds:
                    if not j.startswith('-'):
                        if j in lines[i] and loggedTime:
                            res.append([
                                i + 1,
                                datetime.datetime.strptime(
                                    loggedTime[0], '%Y-%m-%d %H:%M:%S')
                            ])
                            break
                    else:
                        if loggedTime:
                            if j[1:] not in lines[i]:
                                res.append([
                                    i + 1,
                                    datetime.datetime.strptime(
                                        loggedTime[0], '%Y-%m-%d %H:%M:%S')
                                ])
                            break

            if len(params) > 0 and len(res) > 0:
                if 'since' in params.keys() or 'until' in params.keys():
                    timeFrom = params.get('since', None)
                    timeUntil = params.get('until', None)
                    if not timeUntil:
                        endTime = datetime.datetime.now()
                    else:
                        timeUntil = timeFrom.strip() + ' 23:59:59'
                        endTime = datetime.datetime.strptime(
                            timeUntil, '%Y-%m-%d %H:%M:%S')

                    if not timeFrom:
                        startTime = datetime.datetime.strptime(
                            ('1970-01-01 00:00:00'), '%Y-%m-%d %H:%M:%S')
                    else:
                        timeFrom = timeFrom.strip() + ' 00:00:00'
                        startTime = datetime.datetime.strptime(
                            timeFrom, '%Y-%m-%d %H:%M:%S')

                    if not startTime < endTime:
                        print(
                            'time from must less than time until but got {},{}'
                            .format(timeFrom, timeUntil))
                        return

                    filtRes = []
                    for i in res:
                        if i[1] >= startTime and i[1] <= endTime:
                            filtRes.append(i[0])

                    print(filtRes)
                else:
                    print(list(params.keys()))
                    print(
                        'Params error. func "logFilter" needs "until" or "since", got "{}"'
                        .format(' '.join(list(params.keys()))))
                    return

    @classmethod
    @infoDecorate(message='this function is not as good as i supposed.')
    def treeWithState(cls, moduleName):
        if cls.currentModulePath == '':
            module = importlib.__import__(moduleName)
            modulePath = os.path.dirname(module.__file__)
        else:
            modulePath = cls.currentModulePath

        if len(cls.storage) == 0:
            print('Plz run DevTool.exec() first.')

        for root, _, files in os.walk(modulePath):
            level = root.replace(modulePath, '').count(os.sep)
            dir_indent = "|   " * (level - 1) + "|-- "
            file_indent = "|   " * level + "|-- "
            if not level:
                print('.')
            else:
                tmp = os.path.basename(root)
                if tmp != '__pycache__':
                    print('{}{}'.format(dir_indent, os.path.basename(root)))
                del tmp
            for f in files:
                tmp, _ = os.path.splitext(
                    (root + os.sep + f).replace(modulePath,
                                                '').replace(os.sep, '.'))
                if not f.endswith('.pyc'):
                    lastText = ''
                    if len(cls.storage) > 0:
                        for i in cls.storage:
                            tmpModu = i.func.__module__
                            if tmpModu == moduleName + tmp:
                                if __current_platform__ == 'Windows':
                                    text = '{}{}'.format(
                                        file_indent,
                                        f + " --> " + i.funcName + ' --> ' +
                                        str(len(i.func.__annotations__)))
                                else:
                                    text = colored('{}{}'.format(
                                        file_indent,
                                        f + " --> " + i.funcName + ' --> ' +
                                        str(len(i.func.__annotations__))),
                                                   'red',
                                                   attrs=['reverse', 'blink'])
                                print(text) if lastText != text else do_nothing
                                lastText = text
                            else:
                                print('{}{}'.format(
                                    file_indent,
                                    f)) if lastText != '{}{}'.format(
                                        file_indent, f) else do_nothing
                                lastText = '{}{}'.format(file_indent, f)
                    else:
                        print('{}{}'.format(file_indent,
                                            f)) if lastText != '{}{}'.format(
                                                file_indent, f) else do_nothing
                        lastText = '{}{}'.format(file_indent, f)

    @staticmethod
    @logit()
    def initProject(projectName, path='', style='MINE', tree=False):
        if path == '':
            print(
                'This script needs a parameter "path",but got "",using {} instead.'
                .format(BASE_DIR + os.sep + projectName))
            projectPath = BASE_DIR + os.sep + projectName
        else:
            projectPath = path + os.sep + projectName

        if not os.path.exists(projectPath):
            os.mkdir(projectPath)

        # main.py
        f = open(yamlFilePath, 'r', encoding='utf-8', errors='ignore')
        cont = f.read()

        x = yaml.load(cont, Loader=yaml.BaseLoader)

        sty = x[style]
        scripts = sty['scripts']
        folders = sty['folders']
        # print(scripts);print(folders)
        for v in folders.values():
            if not os.path.exists(v.replace('root', projectPath)):
                os.mkdir(v.replace('root', projectPath))
                # print(v.replace('root', projectPath))
        for v in scripts.values():
            if not os.path.exists(v.replace('root', projectPath)):
                # os.mkdir(v.replace('root', projectPath))
                fp = open(v.replace('root', projectPath),
                          'w+',
                          encoding='utf-8')
                fp.close()

        f.close()
        print("Init finishes.")

        if tree:
            for root, _, files in os.walk(projectPath):
                level = root.replace(projectPath, '').count(os.sep)
                dir_indent = "|   " * (level - 1) + "|-- "
                file_indent = "|   " * level + "|-- "
                if not level:
                    print('.')
                else:
                    tmp = os.path.basename(root)
                    if tmp != '__pycache__':
                        print('{}{}'.format(dir_indent,
                                            os.path.basename(root)))
                    del tmp
                for f in files:
                    if not f.endswith('.pyc'):
                        print('{}{}'.format(file_indent, f))

    @staticmethod
    def show(name: str):
        showScript(name)

    @staticmethod
    def search(name: str):
        moduleList = name.split(" ")
        searchScript(moduleList)
