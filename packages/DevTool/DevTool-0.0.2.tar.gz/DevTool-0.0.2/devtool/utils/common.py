'''
lanhuage: python
Descripttion: 
version: beta
Author: xiaoshuyui
Date: 2021-01-08 09:27:04
LastEditors: xiaoshuyui
LastEditTime: 2021-01-26 14:28:17
'''
import datetime
import os
import re
import time

from devtool.utils.devtool_exceptions import MemoryOutOfThresException

is_psutil_installed = False
is_pynvml_installed = False

try:
    import psutil
    is_psutil_installed = True
except:
    pass

try:
    import pynvml
    is_pynvml_installed = True
except:
    pass

__DEFAULT_SIZE__ = 1024 * 1024

memorys = []
memory_percents = []
cpu_percents = []
useds = []


def match_datetime(text):
    '''正则表达式提取文本所有日期+时间

    :param text: 待检索文本

    >>> match_datetime('日期是2020-05-20 13:14:15.477062.')
    ['2020-05-20 13:14:15']
    '''
    pattern = r'(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})'
    pattern = re.compile(pattern)
    result = pattern.findall(text)
    return result


def validate_datetime(text):
    '''验证日期+时间格式

    :param text: 待检索文本

    >>> validate_datetime('2020-05-20 13:14:15')
    True
    >>> validate_datetime('2020-05-32 13:14:15')
    False
    '''
    try:
        if text != datetime.datetime.strptime(
                text, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S'):
            raise ValueError
        return True
    except ValueError:
        return False


def validate_date(text):
    '''验证日期+时间格式

    :param text: 待检索文本

    >>> validate_date('2020-05-20')
    True
    >>> validate_date('2020-05-32')
    False
    '''
    try:
        if text != datetime.datetime.strptime(text,
                                              '%Y-%m-%d').strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False


def showPsInfo_before():
    if not is_psutil_installed:
        print('Module "psutil" is not installed. Plz install it first.')
        return
    currentPid = os.getpid()
    pids = psutil.pids()  # for multi processes maybe
    return currentPid, pids


def situation(beforePids: tuple,
              gpu=False,
              return_dict=dict(),
              mThres=float('inf')):
    global memorys, memory_percents, cpu_percents, useds
    currentPid = beforePids[0]
    # print(currentPid)
    # print(os.getpid())
    p = psutil.Process(currentPid)
    usedMemory = int(psutil.virtual_memory()[0] * p.memory_percent() /
                     (100 * __DEFAULT_SIZE__))
    print("memory : {}, memory_persent : {}, cpu_percent : {}".format(
        str(usedMemory) + "MB",
        str(round(p.memory_percent(), 3)) + "%", p.cpu_percent()))
    memorys.append(usedMemory)
    memory_percents.append(round(p.memory_percent(), 3))
    cpu_percents.append(p.cpu_percent())
    return_dict['memorys'] = memorys
    return_dict['memory_percents'] = memory_percents
    return_dict['cpu_percents'] = cpu_percents

    if usedMemory > mThres:
        print(
            "This function out of memory with threshold {} MB, but got {} MB during runtime."
            .format(mThres, usedMemory))
        mp = psutil.Process(os.getpid())
        p.kill()
        mp.kill()

    if gpu:
        if not is_pynvml_installed:
            print('Module "pynvml" is not installed. Plz install it first.')
        else:
            try:
                pynvml.nvmlInit()
                driver = pynvml.nvmlSystemGetDriverVersion()
                gpunum = pynvml.nvmlDeviceGetCount()
                handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                device = pynvml.nvmlDeviceGetName(handle)
                info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                total = int(info.total / __DEFAULT_SIZE__)
                used = int(info.used / __DEFAULT_SIZE__)
                pynvml.nvmlShutdown()
                print(
                    "driver:{}, gpunum:{}, device:{}, total:{}MB, used:{}MB .".
                    format(driver.decode(), gpunum, device.decode(), total,
                           used))
                useds.append(used)
                return_dict['useds'] = useds  # gpu used not OK
            except:
                print('"pynvml" not working')
    time.sleep(1)


def showPsInfo_after(beforePids: tuple,
                     psname='python',
                     gpu=False,
                     repeat=True,
                     return_dict=dict(),
                     mThres=float('inf')):
    """mThres : memory thres
    """
    if not is_psutil_installed:
        print('Module "psutil" is not installed. Plz install it first.')
        return

    if not repeat:
        situation(beforePids, gpu, return_dict, mThres)
    else:
        while 1 == 1:
            situation(beforePids, gpu, return_dict, mThres)


def plotBeautify(code: str, defaultLength: int = 22):
    assert type(
        code) is str, "param 'code' must be a str, while got a {}".format(
            type(code))
    if len(code) >= defaultLength:
        return code
    else:
        s = len(str(code))
        if s%2 == 0:
            return int(defaultLength / 2 - 0.5 * s - 1) * ' ' + str(
                code) + int(defaultLength / 2 - 0.5 * s) * ' '
        else:
            return int(defaultLength / 2 - 0.5 * s) * ' ' + str(
                code) + int(defaultLength / 2 - 0.5 * s) * ' '
