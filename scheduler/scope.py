# -*- coding: utf-8 -*-
import time
from crawler.settings import CRAWLED_LINK_COUNT_DAY

class Scope(object):
    __shared_state = {}
    
    def __init__(self):
        self.__dict__ = self.__shared_state
    
    
    def frequency_of(self):
        hour = time.strftime('%H',time.localtime(time.time()))
        hour = float(hour)
        
        if hour <= 6:
            return (6 * 3600.0) / (CRAWLED_LINK_COUNT_DAY * 0.1) 
        elif hour <= 12:
            return (6 * 3600.0) / (CRAWLED_LINK_COUNT_DAY * 0.3) 
        elif hour <= 18 :
            return (6 * 3600.0) / (CRAWLED_LINK_COUNT_DAY * 0.4) 
        else:
            return (6 * 3600.0) / (CRAWLED_LINK_COUNT_DAY * 0.2) 
            
            
if __name__ == "__main__":
    scope = Scope()
    print scope.frequency_of()
    hour = 6
    
    