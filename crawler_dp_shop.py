#-*- coding: utf-8 -*-
from Queue import Queue

from core.download_worker import DownloadWorker
from core.extractor_worker import ExtractorWorker
from core.proxy_check_worker import ProxyCheckWorker
from core.queue_monitor import QueueMonitor
from queue.pressure_queue import PressureControlQueue

from settings import DOWNLOAD_WORKERS_SIZE,LINKS_QUEUE_MIN_SIZE,EXTRACTOR_WORKERS_SIZE,PROXY_CHECKER_SIZE
from queue.http_proxy_queue import HttpProxyQueue
from util.data_service import DataService
from util.prase_dp_shop import PraseShop
import logger

class Crawler():
    """
    Main Thread
    """
    def __init__(self):
        self.proxy_queue    = HttpProxyQueue()
        self.links_queue    = PressureControlQueue()
        self.pages_queue    = Queue()

        self.threads    = []
        self.runable    = True
        self.download_workers   = []
        self.extractor_workers  = []

    def start(self):
        self._start_workers()
        self._start_extractors()
        self._start_queue_monitor()
        self._start_proxy_check_workers()

    def _start_proxy_check_worker(self):
        worker = ProxyCheckWorker(self.proxy_queue,PraseShop.check_proxy_available)
        # worker.setDaemon(True)
        worker.start()
        self.threads.append(worker)

    def _start_workers(self):
        for _ in range(DOWNLOAD_WORKERS_SIZE):
            self._start_new_worker()

    def _start_extractors(self):
        for _ in range(EXTRACTOR_WORKERS_SIZE):
            self._start_new_extractor()

    def _start_queue_monitor(self):
        self._start_monitor()

    def _start_proxy_check_workers(self):
        for _ in range(PROXY_CHECKER_SIZE):
            self._start_new_proxy_checker()

    def _start_monitor(self):
        worker = QueueMonitor(self,DataService.add_dp_shop_job,LINKS_QUEUE_MIN_SIZE,DOWNLOAD_WORKERS_SIZE)
        #worker.setDaemon(True)
        worker.start()
        self.threads.append(worker)


    #启动检测http代理的线程
    def _start_new_proxy_checker(self):
        worker = ProxyCheckWorker(self.proxy_queue,PraseShop.check_proxy_available)
        #worker.setDaemon(True)
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
        worker = ExtractorWorker(self.pages_queue,PraseShop.if_has_data,PraseShop.parse_content,DataService.update_dp_shop_task)
        #worker.setDaemon(True)
        worker.start()
        self.extractor_workers.append(worker)


if __name__ == "__main__":
    crawler = Crawler()
    crawler.start()
