# -*- coding:utf-8 -*-
import sys
sys.path.append('..')
url_station = "https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no=%s&from_station_telecode=%s&to_station_telecode=%s&depart_date=%s"

class TrainTask(object):

    def __init__(self,start_station,end_station,train_no,useful_date,train_code,task_id,status,nice,selected,http_code):
        self.start_station = start_station
        self.end_station = end_station
        self.train_no = train_no
        self.task_id = task_id
        self.train_code = train_code
        self.fetched_date = useful_date
        self.status = status
        self.nice = nice
        self.selected = selected
        self.http_code = http_code
        self.url = self.__create_url()


    def __create_url(self):
        url = url_station % (self.train_no,self.start_station,self.end_station,self.fetched_date)
        return url

if __name__ == '__main__':
    a = TrainTask()