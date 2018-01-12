#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Yaro

# Linux 版本的程序
# taskMnager.py for linux

# from queue import Queue
from multiprocessing import Queue

from multiprocessing.managers import BaseManager

# 第一步：建立task_queue and result_queue，用来存放任务和结果
task_queue = Queue()
result_queue = Queue()


class Queue_manager(BaseManager):
    pass


# 第二步：把创建的两个queue注册在网络上，利用register方法，callable参数关联了Queue对象
# 把Queue对象在网络中暴露
Queue_manager.register('get_task_queue', callable=lambda: task_queue)
Queue_manager.register('get_result_queue', callable=lambda: result_queue)

# 第三步：绑定端口8001，设置验证口令'qiye'。这个相当于对象的初始化
manager = Queue_manager(address=('', 8001), authkey='qiye')

# 第四步：启动管理，监听信息通道
manager.start()



