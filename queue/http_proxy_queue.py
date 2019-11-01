# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from Queue import PriorityQueue
from Queue import Queue
from settings import PROXY_FREQUENCY_TIME
import time
import threading
import logging as log


class HttpProxyQueue(object):
    __shared_state = {}
    proxy_checked_queue = Queue()
    proxy_priority_queue = PriorityQueue()
    '''可用代理队列数量'''
    qsize = 0
    _qsize_lock = threading.Condition(threading.Lock())
    '''待检测队列数量'''
    checked_qsize = 0
    _checked_queue_lock = threading.Lock()
    _checked_qsize_lock = threading.Lock()
    ''''''
    _lock  = threading.Condition(threading.Lock())
    _queue_lock  = threading.Condition(threading.Lock())

    def __init__(self):
        self.__dict__ = self.__shared_state
        
        
    def get(self):
        with self._lock:
            while True:
                current = time.time()
                if self._has_pending_site_until(current):
                    proxy_job = self.pop_proxy()
                    log.info("HttpProxyQueue proxy=%s:%s , delay_time=%d/%d" % (proxy_job.ip, proxy_job.port, current, proxy_job.tick_time))
                    return proxy_job
                time.sleep(1)
    
    
    def statics(self):
        with self._queue_lock:
            return "proxys queue size : %d" % self.proxy_priority_queue.qsize()
    
    
    '''弹出一个可用的代理'''
    def pop_proxy(self):
        proxy_job = self.proxy_priority_queue.get(True, 3)
        with self._qsize_lock:
            self.qsize -= 1
        return proxy_job
    
    
    '''向队列中加入一个可用的代理'''
    def put_proxy(self, proxy_job, delay=0):
        with self._queue_lock:
            proxy_job.tick_time += (PROXY_FREQUENCY_TIME + delay)
            self.proxy_priority_queue.put(proxy_job)
            with self._qsize_lock:
                self.qsize += 1
                
                
    '''弹出一个待检测的代理'''
    def pop_checked_proxy(self):
#        with self._checked_queue_lock:
        proxy_job = self.proxy_checked_queue.get(True)
        self.checked_qsize -= 1
        return proxy_job
    
    
    '''向队列中加入一个待检测的代理'''
    def put_checked_proxy(self, proxy_job):
        with self._checked_queue_lock:
            self.proxy_checked_queue.put(proxy_job)
            with self._checked_qsize_lock:
                self.checked_qsize += 1
        
        
    '''检测时间'''
    def _has_pending_site_until(self, current):
        if self.proxy_priority_queue.empty():
            return False
        return current >= self.proxy_priority_queue.queue[0].tick_time
    
