# -*- coding: utf-8 -*-
class PageJob(object):
    def __init__(self, link_job, content=None):
        self.link_job = link_job
        self.content = content
        
    def content_is_empty(self):
        if self.content:
            return False
        else:
            return True
        
