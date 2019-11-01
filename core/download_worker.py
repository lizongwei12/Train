# -*- coding: utf-8 -*-
import pycurl
import random
import socket
import sys
import threading
import traceback
from copy import copy
import urllib
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import logging as log
import mycurl
from job.page_job import PageJob

from errors import HostResolvedError, TimeoutError
from settings import DOWNLOAD_HEADERS, PC_USER_AGENTS_SUM,\
    PC_USER_AGENTS,OK_CODE, NOT_FOUND, \
    IF_USE_PROXY


class DownloadWorker(threading.Thread):
    
    def __init__(self, crawler):
        threading.Thread.__init__(self)
        self.links_queue = crawler.links_queue
        self.pages_queue = crawler.pages_queue
        if IF_USE_PROXY:
            self.proxy_queue = crawler.proxy_queue
    def run(self):
        while True:
            try:
                link_job = self.links_queue.get()
                page_job = PageJob(link_job)
                proxy_job = None
                if IF_USE_PROXY:
                    proxy_job = self.proxy_queue.get()
                status, content = self._download_ssl(link_job)
                if status == OK_CODE:
                    page_job.content = content
                    link_job.http_code = OK_CODE
                elif status == NOT_FOUND:
                    link_job.http_code = NOT_FOUND
            except HostResolvedError:
                log.info("dnserr %s" % link_job.url)
            except TimeoutError:
                log.info("timeout %s" % link_job.url)
            except:
                try:
                    t, v, tb = sys.exc_info()
                    log.info("%s,%s,%s,%s" % (link_job.url, t, v, traceback.format_tb(tb)))
                except:
                    log.info("%s,%s,%s" % (t, v, traceback.format_tb(tb)))
            finally:
                # 代理回收
                if IF_USE_PROXY:
                    if not link_job.http_code == OK_CODE:
                        self.proxy_queue.put_checked_proxy(proxy_job)
                    else:
                        self.proxy_queue.put_proxy(proxy_job)
                self.pages_queue.put(page_job)
                    
    def _download(self, link_job, proxy=None):
        response = None
        proxy_job = None
        if proxy:
            proxy_job ='%s:%s' % (proxy.ip,proxy.port)
        try:
            headers = copy(DOWNLOAD_HEADERS)
            headers.append(self.__shuffle_pc_user_agent())
            response = mycurl.get(link_job.url, timeout=20, request_headers=headers,proxy=proxy_job)
        except socket.gaierror:
            raise HostResolvedError
        except pycurl.error, e:
            log.info("Download error %s [%s] for url [%s] with proxy [%s]" % (e[0], e[1], link_job.url, proxy_job))
        
        if response and response.status:
            status = response.status
            body_length = len(response.body)
        else:
            status, response, body_length = None, None, None
            
        log.info('Download url=%s, status=%s, response=%s, bodylength=%s, proxy=%s' % (link_job.url, status, response, body_length, proxy_job))
        return status, response

    def _download_ssl(self,link_job):
        content = None
        status = None
        response = None
        try:
            # headers = copy(DOWNLOAD_HEADERS)
            # headers.append(self.__shuffle_pc_user_agent())
            response = urllib.urlopen(link_job.url)
            content = response.read()
            response.close()
            status = response.code
        except Exception as e:
            log.info("Download error %s [%s] for url [%s] with proxy [%s]" % (e[0], e[1], link_job.url, 'None'))

        if content and status:
            body_length = len(content)
        else:
            status, response, body_length = None, None, None
        log.info('Download url=%s, status=%s, response=%s, bodylength=%s, proxy=%s' % (link_job.url, status, response, body_length, 'none'))
        return status, content

    def __shuffle_pc_user_agent(self):
        index = random.randint(0, PC_USER_AGENTS_SUM - 1)
        return "User-Agent: %s" % PC_USER_AGENTS[index]


