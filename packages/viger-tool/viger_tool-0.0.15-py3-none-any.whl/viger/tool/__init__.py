#!/usr/bin/env python

"""
author: walker
description:
    Python 工具包
change log:
    2019-12-29 init
    2020-01-17 Add Requests Class
    2020-02-01 Add logrotate Function
    2020-04-19 增加Param類型判斷
    2021-01-19 調整json默認編碼
"""

import io
import os
import sys
import time
import shutil
import requests
import traceback
import prettytable as pt
from datetime import datetime, timedelta

from . import logging
from .mail import Mail
from .timer import Timer
from .json import json
from .encryption import pass_encode, pass_decode

def logrotate(target, interval=timedelta(days=1), time_format='%Y%m%d'):
    """
    日志切割
    :param target(str): 目标文件夹or日志
    :param interval(timedelta): 切割间隔
    :param time_format(str): 文件名日期格式
    :return: None
    """
    if os.path.isfile(target):
        path = ''
        files = [target]
    else:
        path = target if target[-1] == '/' else target + '/'
        files = os.listdir(target)

    for f in files:
        segment = f.split('.')
        if len(segment) != 2 or segment[-1] != 'log':
            continue
        flag = (datetime.now() - interval).strftime(time_format)
        src = path + f
        dst = path + '{}.{}.{}'.format(segment[0], flag, segment[1])
        if os.path.exists(dst):
            continue
        shutil.copyfile(src, dst)
        with open(src, 'w') as f:
            pass

def print_table(header, data, sort=None):
    """
    字典列表，输出成表格形式
    """
    tb = pt.PrettyTable()
    tb.field_names = header
    for d in data:
        tb.add_row([d[h] for h in header])
    tb.align = 'l'
    if sort is not None:
        tb.sortby = header[sort]
    print(tb)

# Format Request
class Requests():
    """
    包裝request方法，
    只支援JSON格式，
    return Result
    """
    def __init__(self, *args, **kwargs):
        # 取消告警
        requests.packages.urllib3.disable_warnings()

        self.header = {
            'Content-Type': 'application/json',
        }
        self.timeout = kwargs.get('timeout', 10)
        self.result = Result()

    def get(self, url, body={}):
        """
        通用Get方法
        """
        try:
            resp = requests.get(url, json=body, headers=self.header, 
                    timeout=self.timeout, verify=False)
            if resp.status_code != 200:
                self.result.set(resp.text, False)
                return self.result
            self.result.set(json.loads(resp.text))
        except json.decoder.JSONDecodeError:
            self.result.set(resp.text, False)
        except Exception as e:
            self.result.set(str(e), False)
        return self.result

    def post(self, url, body=None):
        """
        通用Post方法
        """
        try:
            resp = requests.post(url, json=body, headers=self.header,
                    timeout=self.timeout, verify=False)
            if resp.status_code not in [200, 201, 202, 204]:
                self.result.set(resp.text, False)
                return self.result
            self.result.set(json.loads(resp.text))
        except json.decoder.JSONDecodeError:
            self.result.set(resp.text, False)
        except Exception as e:
            self.result.set(str(e), False)
        return self.result

    def put(self, url, body=None):
        """
        通用Put方法
        """
        try:
            resp = requests.put(url, json=body, headers=self.header,
                    timeout=self.timeout, verify=False)
            if resp.status_code not in [200, 201, 202, 204]:
                self.result.set(resp.text, False)
                return self.result
            self.result.set(json.loads(resp.text))
        except json.decoder.JSONDecodeError:
            self.result.set(resp.text, False)
        except Exception as e:
            self.result.set(str(e), False)
        return self.result

    def delete(self, url, body=None):
        """
        通用Delete方法
        """
        try:
            resp = requests.delete(url, json=body, headers=self.header,
                    timeout=self.timeout, verify=False)
            if resp.status_code not in [200, 201, 202, 204]:
                self.result.set(resp.text, False)
                return self.result
            if resp.text:
                self.result.set(json.loads(resp.text))
            else:
                self.result.set('')
        except json.decoder.JSONDecodeError:
            self.result.set(resp.text, False)
        except Exception as e:
            self.result.set(str(e), False)
        return self.result

# Parse Argument
class Param():
    """
    参数校验
    """
    def __init__(self, data):
        self._data = data
        self.args = {}

    def __getitem__(self, key):
        return self.args[key]

    def __setitem__(self, key, val):
        self.args[key] = val

    def __len__(self):
        return len(self.args)

    def parse(self, key, default='__placeholder__', type=None):
        """
        参数解析
        :param key(any): 参数
        :param defualt(any): 默认值
        :param type(type): 指定参数类型
        """
        arg = ''
        msg = 'Missing parameters {}'.format(key)
        if key in self._data:
            if self._data[key] == '':
                if default == '__placeholder__':
                    raise ValueError(msg)
                arg = self.define_type(default, type)
            else:
                arg = self.define_type(self._data[key], type)
        else:
            if default == '__placeholder__':
                raise ValueError(msg)
            arg = self.define_type(default, type)
        self.args[key] = arg
        setattr(self, key, arg)

    def define_type(self, value, type):
        """
        类型校验
        """
        msg = 'Type parameter Error'
        if type is None:
            return value
        if type in [str, int, float]:
            return type(value)
        if type in [bool]:
            if value in [0, '', 'False', 'false', False]:
                return False
            else:
                return True
        if type in [list, dict]:
            if isinstance(value, type):
                return value
        raise TypeError(msg)

# Format Result
class Result():
    """
    函数执行结果格式化
    OK: 是否成功(True|False)
    line: 代码哪一行输入
    data: 输出的结果
    time: 从初始化到设值的时间
    """
    OK = True
    line = ''
    data = ''
    time = 0

    def __init__(self):
        self.set_dict()
        self._time = time.time()

    def __str__(self):
        if isinstance(self.data, str):
            return self.data
        elif isinstance(self.data, list):
            return json.dumps(self.data, indent=2, ensure_ascii=False)
        elif isinstance(self.data, dict):
            return json.dumps(self.data, indent=2, ensure_ascii=False)
        else:
            return str(self.data)

    def __repr__(self):
        return self.__str__()

    def set(self, data, OK=True):
        filename = sys._getframe(1).f_code.co_filename
        line = sys._getframe(1).f_lineno

        self.OK = OK
        self.line = '{}(line:{})'.format(filename, line)
        self.data = data
        self.time = '%0.3f'%(time.time() - self._time)
        self.set_dict()

    def set_dict(self):
        self.dict = {
            'OK': self.OK,
            'line': self.line,
            'data': self.data,
            'time': self.time,
        }

    def __getitem__(self, key):
        return self.dict[key]

    def __setitem__(self, key, value):
        self.dict[key] = value

    def __len__(self):
        return len(self.dict)

    def __contains__(self, key):
        return key in self.dict

# 客制化 Logger
class Logger(logging.Logger):
    """
    獲取logger，格式化日志輸出
    ex:
        logger = Logger('tool', 'stream')
        logger.info('Hello')

    >> 2020-03-10 00:36:10,873のINFOのtoolの./tool.py(line:299)のHello
    """

    PATH = sys.path[0] + '/logs/'
    LOG_FILE = '%s%s.log'%(PATH, datetime.now().strftime('%Y%m%d'))
    LOG_FORMAT = '%(asctime)sの%(levelname)sの%(name)sの%(pathname)s(line:%(lineno)d)の%(message)s'

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        cls.__init__(obj, *args, **kwargs)
        return obj.logger

    def __init__(self, name='root', type='stream', level='info'):
        """
        :param name(str): Log Name
        :param type(str): Log Type: print, stream, file
        :param level(str): Log Level: critical, error, warn, info, debug
        """
        super().__init__(name, level.upper())
        func = getattr(self, f'{type}_logger')
        self.logger = func(name, level)

    def file_handler(self, logfile=LOG_FILE):
        if not os.path.isdir(self.PATH):
            os.makedirs(self.PATH)
        _format = self.LOG_FORMAT
        handler = logging.FileHandler(logfile)
        formatter = logging.Formatter(_format)
        handler.setFormatter(formatter)
        return handler

    def stream_handler(self):
        _format = self.LOG_FORMAT
        handler = logging.StreamHandler()
        formatter = logging.Formatter(_format)
        handler.setFormatter(formatter)
        return handler

    def print_handler(self):
        _format = '%(message)s'
        handler = logging.StreamHandler()
        formatter = logging.Formatter(_format)
        handler.setFormatter(formatter)
        return handler

    def file_logger(self, obj='__main__', level='info', logfile=LOG_FILE):
        handler = self.file_handler(logfile)
        logger = logging.getLogger(obj)
        logger.setLevel(level.upper())
        logger.addHandler(handler)
        return logger

    def stream_logger(self, obj='__main__', level='info'):
        handler = self.stream_handler()
        logger = logging.getLogger(obj)
        logger.setLevel(level.upper())
        logger.addHandler(handler)
        return logger

    def print_logger(self, obj='__main__', level='info'):
        handler = self.print_handler()
        logger = logging.getLogger(obj)
        logger.setLevel(level.upper())
        logger.addHandler(handler)
        return logger

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info,
                   func=None, extra=None, sinfo=None):
        """
        A factory method which can be overridden in subclasses to create
        specialized LogRecords.
        """
        rv = _logRecordFactory(name, level, fn, lno, msg, args, exc_info, func,
                             sinfo)
        if extra is not None:
            for key in extra:
                # 修正變量無法取代問題
                #if (key in ["message", "asctime"]) or (key in rv.__dict__)
                if (key in ["message", "asctime"]):
                    raise KeyError("Attempt to overwrite %r in LogRecord" % key)
                rv.__dict__[key] = extra[key]
        return rv

if __name__ == '__main__':

    #os.chdir(sys.path[0])
    #logrotate('logs')
    logger = Logger('main')
    logger.info('Hello')
