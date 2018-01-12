#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Yaro

import time
from multiprocessing.managers import BaseManager


# 创建类似的Queue_manager：
class Queue_manager(BaseManager):
    pass


# 第一步：使用Queue_manager注册用于Queue的方法名称
Queue_manager.register('get_task_queue')
Queue_manager.register('get_result_queue')

# 第二步：连接到服务器
server_addr = '127.0.0.1'
print('Connect to server {}'.format(server_addr))

# 端口和验证口令需要与服务端进程完全一致
m = Queue_manager(address=(server_addr, 8001), authkey='qiye')
# 从网络连接
m.connect()

# 第三步：获取Queue的对象：
task = m.get_task_queue()
result = m.get_result_queue()

# 第四步：从task队列获取任务，并把结果写入result队列：
while not task.empty():
    image_url = task.get(True, timeout=5)
    print('run task download {}'.format(image_url))
    time.sleep(1)
    result.put('{} ---> success'.format(image_url))

# 处理结果
print('worker exit.')
