# -*- coding: utf-8 -*-
from job.proxy_job import ProxyJob
from settings import check_url,check_heades
import sys
sys.path.append('..')
import threading
import mycurl
import logging as log
import json


class ProxyCheckWorker(threading.Thread):
    """
        检测失败的代理是否可以重新使用
    """
    def __init__(self, http_proxy_queue,proxy_check_func):
        threading.Thread.__init__(self)
        self.http_proxy_queue = http_proxy_queue
        self.proxy_check_func = proxy_check_func
        
    def run(self):
        while True:
            proxy_job = self.http_proxy_queue.pop_checked_proxy()
            ip, port = proxy_job.ip, proxy_job.port
            flag = self.proxy_check_func(ip, port)
            if flag:
                self.http_proxy_queue.put_proxy(ProxyJob(ip,port))
                log.info("ProxyCheckWorker thread_name = %s, check proxy usable %s:%s ok..." % (threading.current_thread().getName(), ip, port))
            else:
                self.http_proxy_queue.put_checked_proxy(ProxyJob(ip,port))
                log.info("ProxyCheckWorker thread_name = %s, check proxy usable %s:%s error..." % (threading.current_thread().getName(), ip, port))
