#-*- coding: utf-8 -*-
import json
import sys
import traceback
import logging as log
from data_service import DataService
from settings import check_url,check_heades
import mycurl

class PraseList(object):

    shop_url_pattern = "http://www.dianping.com/shop/%s"

    def __init__(self):
        pass

    @classmethod
    def if_has_data(self,content):
        if content:
            try:
                json_obj = json.loads(content)
                if len(json_obj["list"]) != 0:
                    return True
            except:
                pass
        return False

    @classmethod
    def parse_content(self,content,link_job):
        json_obj = json.loads(content)
        list = json_obj['list']
        for shop in list:
            try:
                category_id = shop['categoryId']
                city_id = shop['cityId']
                shop_id = shop['id']
                url = self.shop_url_pattern %  shop_id
                DataService.save_dp_shop(url,shop_id,city_id,category_id)
            except:
                t, v, tb = sys.exc_info()
                log.error("%s,%s,%s" % (t, v, traceback.format_tb(tb)))

    @classmethod
    def check_proxy_available(cls,ip, port):
        flag = False
        try:
            response = mycurl.get(check_url,request_headers=check_heades,timeout=5, proxy="%s:%s" % (ip,port))
            if response.status == 200:
                content = response.body
                if content:
                    json_obj = json.loads(content)
                    if json_obj["recordCount"]:
                        flag = True
        except:
            pass
        return flag