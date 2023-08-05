#! /usr/bin/env python
__author__ = 'Tser'
__email__ = '807447312@qq.com'
__project__ = 'xiaobaiauto2'
__script__ = 'xiaobaiauto2App.py'
__create_time__ = '2020/12/29 21:41'

import os
from argparse import ArgumentParser
from xiaobaiauto2.utils.xiaobaiauto2Subprocess import syncSub, devices
from xiaobaiauto2.__version__ import __version__
from xiaobaiauto2.utils import grep, _get_path

def adb_cmd():
    ADB_COMMAND = f'"{_get_path("adb")}" '
    arg = ArgumentParser(prog='xiaobaiauto2App [optional] [command]',
                         description=f'小白科技·移动设备调试桥·{__version__}')
    arg.add_argument('-d', '--deviceName', default='')
    arg.add_argument('-i', '--index', default=0, type=int, help='设备索引')
    par = arg.parse_args()
    syncSub(ADB_COMMAND + 'devices -l', match='(\S+)\s+device\s+', other='device')
    print(devices)
    if par.deviceName == '' and isinstance(devices, list) and devices.__len__() > 0 or\
        par.deviceName != '' and par.deviceName not in devices:
        deviceName = '-s ' + devices[par.index]
    elif par.deviceName != '' and isinstance(devices, list) and devices.__len__() > 0 and par.deviceName in devices:
        deviceName = '-s ' + par.deviceName
    else:
        deviceName = ''
    version = os.popen(cmd=f'{ADB_COMMAND}{deviceName} shell getprop ro.build.version.release').read()
    if os.name == 'nt':
        syncSub(f'{ADB_COMMAND}{deviceName} shell getevent -p',
                match='003[56]\s+.+max\s+(\d+)', other='size', deviceName=deviceName)
    else:
        syncSub(f'{ADB_COMMAND}{deviceName} shell getevent -p' + f'| {grep} -e "0035" -e "0036" | {grep} -e "max"',
                match='003[56]\s+.+max\s+(\d+)', other='size', deviceName=deviceName)
    if version >= '8.1':
        syncSub(f'{ADB_COMMAND}{deviceName} shell dumpsys activity | grep ' + '"mResume"',
                match='([\.0-9a-zA-Z]+?/[\.0-9a-zA-Z]+)', other='activity', deviceName=deviceName)
    else:
        syncSub(f'{ADB_COMMAND}{deviceName} shell dumpsys activity | grep ' + '"mFocus"',
                match='([\.0-9a-zA-Z]+?/[\.0-9a-zA-Z]+)', other='activity', deviceName=deviceName)
    try:
        syncSub(f'{ADB_COMMAND}{deviceName} shell getevent',
                match='003[56]\s+[0]+([0-9a-f]+)', other='getevent', deviceName=deviceName)
    except KeyboardInterrupt as e:
        print('您已经手动终止进程.')