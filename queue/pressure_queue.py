# -*- coding: utf-8 -*-
import threading
import time
from Queue import PriorityQueue

from settings import FREQUENCY_TIME


class PressureControlQueue(object):
    __shared_state = {}
    link_priority_queue = PriorityQueue()
    qsize = 0

    
    
    def __init__(self):
        self.__dict__ = self.__shared_state
        self._lock = threading.Lock()
        self._qsize_lock = threading.Lock()
        self._queue_lock = threading.Lock()
        self.tick_time = time.time()
        
        
    def get(self):
        with self._lock:
            while True:
                current = time.time()
                if self._has_pending_site_until(current):
                    link_job = self.pop_link()
                    return link_job
                time.sleep(0.2)
    
    def statics(self):
        with self._queue_lock:
            return "links queue size : %d" % self.link_priority_queue.qsize()
    
    def pop_link(self):
        link_job = self.link_priority_queue.get(True, 3)
        with self._qsize_lock:
            self.qsize -= 1
        return link_job
    
    def put_link(self, link_job):
        with self._queue_lock:
            self.tick_time += FREQUENCY_TIME
            link_job.tick_time = self.tick_time
            self.link_priority_queue.put(link_job)
            with self._qsize_lock:
                self.qsize += 1
        
    def _has_pending_site_until(self, current):
        if self.link_priority_queue.empty():
            return False
        return current >= self.link_priority_queue.queue[0].tick_time
    
    