# -*- coding:utf-8 -*-

class DPListTask(object):
    def __init__(self,task_id,url,status,nice,selected,http_code):
        self.url = url
        self.task_id = task_id
        self.status = status
        self.nice = nice
        self.selected = selected
        self.http_code = http_code
        self.fetched_date = '2017-05-19'


class DPShopTask(object):
    def __init__(self,url_id,url,shop_id,city_id,category_id,status, nice, selected, http_code):

        self.task_id = url_id
        self.url = url
        self.shop_id = shop_id
        self.city_id = city_id
        self.category_id = category_id
        self.status = status
        self.nice = nice
        self.selected = selected
        self.http_code = http_code
        self.fetched_date = '2017-05-19'