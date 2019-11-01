#-*- coding: utf-8 -*-
from Queue import Queue

from core.download_worker import DownloadWorker
from core.extractor_worker import ExtractorWorker
from core.proxy_check_worker import ProxyCheckWorker
from core.queue_monitor import QueueMonitor
from queue.pressure_queue import PressureControlQueue

from settings import LINKS_QUEUE_MIN_SIZE
from util.data_service import DataService
from util.prase_station_12306 import ParseStation
import logger

class Crawler():
    """
    Main Thread
    """
    def __init__(self):
        self.links_queue    = PressureControlQueue()
        self.pages_queue    = Queue()
        
        self.threads    = []
        self.download_workers   = []
        self.extractor_workers  = []
        
    def start(self):
        self._start_workers()
        self._start_extractors()
        self._start_queue_monitor()


    def _start_workers(self):
        for _ in range(1):
            self._start_new_worker()

    def _start_extractors(self):
        for _ in range(1):
            self._start_new_extractor()

    def _start_queue_monitor(self):
        self._start_monitor()


    def _start_monitor(self):
        worker = QueueMonitor(self,DataService.add_train_job,LINKS_QUEUE_MIN_SIZE,1)
        # worker.setDaemon(True)
        worker.start()
        self.threads.append(worker)


    #启动下载线程
    def _start_new_worker(self):
        worker = DownloadWorker(self)
        #worker.setDaemon(True)
        worker.start()
        self.download_workers.append(worker)

    #启动解析线程
    def _start_new_extractor(self):
        worker = ExtractorWorker(self.pages_queue,ParseStation.if_has_data,ParseStation.parse_content,DataService.update_train_task)
        #worker.setDaemon(True)
        worker.start()
        self.extractor_workers.append(worker)
if __name__ == "__main__":
    crawler = Crawler()
    crawler.start()
    