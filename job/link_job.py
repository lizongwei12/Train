# -*- coding: utf-8 -*-
import time

class LinkJob(object):
    
    def __init__(self, task):
        self.task_id = task.task_id
        self.url = task.url
        self.tick_time = time.time()
        self.http_code =task.http_code
        self.status = task.status
        self.nice = task.nice
        self.fetched_date = task.fetched_date
        self.task = task
    
    def __cmp__(self, link_job):
        if isinstance(link_job, LinkJob):
            return cmp(self.tick_time, link_job.tick_time)
        else:
            return -1
