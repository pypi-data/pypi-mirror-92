#! /usr/bin/env python
__author__ = 'Tser'
__email__ = '807447312@qq.com'
__project__ = 'xiaobaiauto2'
__script__ = 'xiaobaiauto2Subprocess.py'
__create_time__ = '2021/1/4 17:13'

import subprocess
import shlex
import re
from datetime import datetime
from xiaobaiauto2.utils import _get_xpath, del_temp

devices = []

def syncSub(cmd=None, match=None, other=None, deviceName=None):
    if cmd:
        global devices
        all_r = []
        p = subprocess.Popen(shlex.split(cmd), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while p.poll() is None:
            l = p.stdout.readline()
            l = l.strip()
            if l and match and other == 'getevent':
                r = [int(v, 16) for v in re.findall(match, str(l, encoding='utf-8'))]
                if r != [] and r != b'' and r != [0]:
                    all_r.extend(r)
            elif l and match and other:
                r = re.findall(match, str(l, encoding='utf-8'))
                if r != [] and r != b'' and r != [0]:
                    all_r.extend(r)
            if other == 'device':
                devices.extend(all_r)
                all_r.clear()
            elif other == 'activity':
                try:
                    print(f'[{datetime.now()}]\t[{str(deviceName).split(" ")[-1]}]\t{all_r[0]}')
                    all_r.clear()
                except IndexError as e:
                    pass
            elif len(all_r) > 1:
                if other == 'getevent':
                    try:
                        xpath = _get_xpath(x=all_r[0], y=all_r[1], deviceName=deviceName)
                        del_temp()
                        print(f'[{datetime.now()}]\t[{str(deviceName).split(" ")[-1]}]\t{all_r}\t{xpath}')
                    except Exception as e:
                        print(f'[{datetime.now()}]\t[{str(deviceName).split(" ")[-1]}]\t{all_r}\t{e}')
                elif other == 'size':
                    print(f'[{datetime.now()}]\t[{str(deviceName).split(" ")[-1]}]\t{all_r}')
                all_r.clear()
        if p.returncode == 0:
            return True
        else:
            return False