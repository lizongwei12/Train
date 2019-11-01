# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
import threading
import traceback
import logging as log
from util import date_util
from settings import STATUS_ERROR,CATCH_NUM,OK_CODE,STATUS_OK,NOT_FOUND,DATE_NEED_ADD
class ExtractorWorker(threading.Thread):
    """
    Extractor Thread: used to send the crawled pages to Extractor.
    监听pages queue，将page中的link抽出，并将当前页面的访问status一同保存到linkbase中
    """
    def __init__(self, pagesQueue,if_has_data_func,parse_content_func,update_task_func):
        threading.Thread.__init__(self)
        #self.client = Client()
        self.pages_queue = pagesQueue
        self.if_has_data = if_has_data_func
        self.parse_content = parse_content_func
        self.update_task = update_task_func

    def run(self):
        while True:
            try:
                page_job = self.pages_queue.get()
                link_job = page_job.link_job
                http_code = link_job.http_code
                link_job.nice += 1
                link_job.selected = 0
                content = page_job.content
                if http_code == OK_CODE and self.if_has_data(content):
                    link_job.status = STATUS_OK
                    self.parse_content(content,link_job)
                else:
                    link_job.http_code = -1
                    if DATE_NEED_ADD:
                        link_job.fetched_date = date_util.increaseDate(link_job.fetched_date) 
                # 抓取catch_num次还未有数据时候，停止抓取
                if link_job.nice > CATCH_NUM:
                    link_job.status = STATUS_ERROR
            except:
                t, v, tb = sys.exc_info()
                log.error("%s,%s,%s" % (t, v, traceback.format_tb(tb)))
            finally:
                self.update_task(link_job.status,link_job.nice,link_job.selected,link_job.fetched_date,link_job.http_code,link_job.task_id)
        log.info("ExtractorWorker Thread[%s] exited." % self.getName())
