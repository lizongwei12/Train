# -*- coding: utf-8 -*-
import logger, mycurl
from extractor.parsers import CtripParser, QunarParser, RailwayParser
#from crawler.settings import REPOSITORY_HOST
import re

gb_header_pattern = re.compile(r'(encoding|charset|content)\s*=\s*["|\']*\s*(gb2312|gbk)', re.I)

encoding_variations = {
    'utf8': 'utf-8',
    'utf-8': 'utf-8',
    'gb2312': 'gb2312',
    'gbk': 'gbk',
}

class Page(object):
    PARSERS = [CtripParser]
    
    def __init__(self, url, page_content, http_headers={}):
        self.url = url
        if 'charset' in http_headers:
            self.encoding = http_headers.get('charset')
        else:
            self.encoding = self.__parse_encoding(page_content)

        self.page_content = self.__clean_decode(page_content)
    
    def __parse_encoding(self, page):
        pattern = re.compile(r'<meta.*(?:(?:charset\s*=\s*["|\']?)|(?:charset.*content\s*=\s*["|\']\s*))([\d|\w|\-]+)[;|"|\'|\s]', re.M + re.I)
        match = pattern.search(page)
        if match:
            charset = match.groups()[0]
            if charset:
                charset = charset.lower()
                return encoding_variations.get(charset, charset)
        return None
    
    def __clean_decode(self, page_content):
        if self.encoding in ['gbk', 'gb18030', 'gb2312'] or gb_header_pattern.search(page_content):
            page_content = page_content.decode('gb18030', 'ignore').encode('utf8')
        elif self.encoding and self.encoding != 'utf-8':
            page_content = page_content.decode(self.encoding, 'ignore').encode('utf8')

        return page_content
    
    def save(self):
        try:
            data = "%s%s%s"%(self.url, '\r\n\r\n', self.page_content.decode('utf8'))
        except:
            data = "%s%s%s"%(self.url, '\r\n\r\n', self.page_content.decode('gb18030', 'ignore'))
        post_url = "http://%s%s" % (REPOSITORY_HOST, "/store")
    
        mycurl.post(url=post_url, data=data.encode('utf8'))

