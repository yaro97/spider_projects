#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Yaro

import os
from multiprocessing import Process


# multiprocessing模块提供Process类描述一个进程对象，创建子进程时，只需要传入一个函数和一个参数，即可完成
# 一个Process实例的创建，用start()方法启动进程，用Join()方法实现进程间的同步。

# 子进程需要执行的代码
def run_proc(name):
    print('Child process {} {} Running...'.format(name, os.getpid()))


if __name__ == '__main__':
    print('Parent process {} is running.'.format(os.getpid()))
    for i in range(5):
        p = Process(target=run_proc, args=(str(i),))
        print('Process will start')
        p.start()
    p.join()
    print('Process end')
