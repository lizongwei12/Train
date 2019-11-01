import pycurl
import socket
from copy import copy
from random import randint

import mycurl
from errors import HostResolvedError
from settings import DOWNLOAD_HEADERS
from user_agents import PC_USER_AGENTS, PC_USER_AGENTS_SUM


class WapDownloader(object):

    def __init__(self, link_job):
        self.link_job = link_job

    def get_response(self):
        response = None
        try:
            headers = copy(DOWNLOAD_HEADERS)
            headers.append(self.__shuffle_pc_user_agent())

            response = mycurl.get_from_link_job(link_job=self.link_job, timeout=15, request_headers=headers)
        except socket.gaierror:
            raise HostResolvedError
        except pycurl.error, e:
            logger.error("Download error %s [%s] for url [%s]" % (e[0], e[1], self.link_job.url))

        if response and response.status:
            return response.status, response
        else:
            return None, None

    def __shuffle_pc_user_agent(self):
        index = randint(0, PC_USER_AGENTS_SUM - 1)
        return "User-Agent: %s" % PC_USER_AGENTS[index]
