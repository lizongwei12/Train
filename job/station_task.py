# -*- coding:utf-8 -*-
import time
import json
class StationTask(object):
    def __init__(self,task_id,begin_stop,ctrip_begin_stop,end_stop,ctrip_end_stop,status,nice,selected,fetched_date,http_code):
        self.task_id = task_id
        self.begin_stop = begin_stop
        self.ctrip_begin_stop = ctrip_begin_stop
        self.end_stop = end_stop
        self.ctrip_end_stop = ctrip_end_stop
        self.fetched_date = fetched_date
        self.status = status
        self.nice = nice
        self.selected = selected
        self.http_code = http_code
        self.url = self.__create_url()


    def __create_url(self):
        millis = int(round(time.time() * 1000))
        callback = "jQuery18309102298273607763_%s" % millis
        para ={"To":self.end_stop,"From":self.begin_stop,"TrainDate":self.fetched_date,"PassType":"","TrainClass":"","FromTimeSlot":"","ToTimeSlot":"","FromStation":"","ToStation":"","SortBy":"fromTime","callback":"","tag":"","memberId":"0","headct":"0","platId":1,"headver":"1.0.0","headtime":int(round(time.time() * 1000))}
        para=json.dumps(para)
        url = "https://www.ly.com/uniontrain/trainapi/TrainPCCommon/SearchTrainRemainderTickets?callback=%s&para=%s"
        url = url % (callback,para)
        return url

if __name__ == '__main__':
    task = StationTask(1,'北京','','上海','',1,1,1,'2017-07-14',1)
    print task.url