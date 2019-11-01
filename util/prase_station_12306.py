#-*- coding: utf-8 -*-
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
import json
import traceback
from data_service import DataService
import logging as log
from pinyin import PinYin
py_util = PinYin()
py_util.load_word('../word.data')
def compareSS(start,end):
    s_min = str(start).split(':')
    e_min = str(end).split(':')
    s_int = int(s_min[0])*60+int(s_min[1])
    e_int = int(e_min[0])*60+int(e_min[1])
    duration = e_int-s_int
    return duration*60

def getDaysSS(start,end,days):
    s_min = str(start).split(':')
    e_min = str(end).split(':')
    s_int = int(s_min[0])*60+int(s_min[1])
    e_int = int(e_min[0])*60+int(e_min[1])
    duration = 0
    if days == 0:
        duration = e_int-s_int
    else:
        duration = e_int+24*60-s_int
    return duration*60
class ParseStation(object):

    @classmethod
    def if_has_data(self,content):
        if content:
            try:
                json_obj = json.loads(content)
                if json_obj['data']:
                    return True
            except:
                pass
        return False

    @classmethod
    def parse_content(self,content,link_job):
        json_obj = json.loads(content)
        data = json_obj['data']['data']
        typeName = data[0]['train_class_name']
        start_time = data[0]['start_time']
        pre_time = start_time
        duration = 0
        name_list = {}
        days = 0
        train_no = link_job.task.train_no
        # 保存站点数据
        for i,d in enumerate(data):
            arrive_time = d['arrive_time']
            depart_time = d['start_time']
            if i==0 :
                arrive_time = 'null'
            if i != 0:
                if compareSS(pre_time,arrive_time)<0:
                    days +=1
                duration = duration + getDaysSS(start_time,d['arrive_time'],days)
                pre_time = arrive_time
                if int(d['station_no'])==1:
                    raise  Exception
            stayTime = 0
            if i!=0 and i!= len(data)-1 :
                stayTime = d['stopover_time']
                try:
                    stayTime = stayTime[0:str(stayTime).index('分')]
                except Exception as e:
                    stayTime=0
                    # raise e
            if i == len(data)-1:
                depart_time = 'null'
            try:
                train_stop = TrainStop(link_job.task.train_code,d['station_name'],int(d['station_no']),arrive_time,stayTime,days,duration,depart_time,typeName,train_no)
                DataService.save_train_stop(train_stop)
                log.info((link_job.task.train_code,d['station_name'],int(d['station_no']),arrive_time,stayTime,days,duration,depart_time,typeName,train_no))
                name_list.update({d['station_no']:d['station_name']})
            except:
                t, v, tb = sys.exc_info()
                log.error("%s,%s,%s" % (t, v, traceback.format_tb(tb)))
        # 保存站到站
        kvs = name_list.items()
        i = -1
        for ki,vi in kvs:
            i += 1
            j = -1
            for kj,vj in  kvs:
                j += 1
                if i == j:
                    continue
                start_station = vi
                end_station = vj
                try:
                    start_py = DataService.get_alia_by_station(start_station)
                    if start_py == '':
                        start_py =  py_util.hanzi2pinyin_split(string=start_station, split="", firstcode=False)
                    end_py = DataService.get_alia_by_station(end_station)
                    if end_py == '':
                        end_py =  py_util.hanzi2pinyin_split(string=end_station, split="", firstcode=False)
                    DataService.save_s2s(start_station,start_py,end_station,end_py)
                except:
                    t, v, tb = sys.exc_info()
                    log.error("%s,%s,%s" % (t, v, traceback.format_tb(tb)))

class TrainStop():
    def __init__(self,train_code,station_name,station_no,arrive_time,stayTime,days,duration,depart_time,typeName,train_no):
        self.train_code = train_code
        self.station_name = station_name
        self.station_no = station_no
        self.arrive_time = arrive_time
        self.stayTime = stayTime
        self.days = days
        self.duration = duration
        self.depart_time =depart_time
        self.typeName = typeName
        self.train_no = train_no

if __name__ == '__main__':
    c='{"validateMessagesShowId":"_validatorMessage","status":true,"httpstatus":200,"data":{"data":[{"start_station_name":"北京南","arrive_time":"----","station_train_code":"G129","station_name":"北京南","train_class_name":"高速","service_type":"1","start_time":"12:10","stopover_time":"----","end_station_name":"上海虹桥","station_no":"01","isEnabled":true},{"arrive_time":"12:44","station_name":"天津南","start_time":"12:46","stopover_time":"2分钟","station_no":"02","isEnabled":true},{"arrive_time":"13:30","station_name":"德州东","start_time":"13:32","stopover_time":"2分钟","station_no":"03","isEnabled":true},{"arrive_time":"13:56","station_name":"济南西","start_time":"13:58","stopover_time":"2分钟","station_no":"04","isEnabled":true},{"arrive_time":"15:01","station_name":"徐州东","start_time":"15:04","stopover_time":"3分钟","station_no":"05","isEnabled":true},{"arrive_time":"15:24","station_name":"宿州东","start_time":"15:26","stopover_time":"2分钟","station_no":"06","isEnabled":true},{"arrive_time":"16:26","station_name":"南京南","start_time":"16:28","stopover_time":"2分钟","station_no":"07","isEnabled":true},{"arrive_time":"16:47","station_name":"镇江南","start_time":"16:49","stopover_time":"2分钟","station_no":"08","isEnabled":true},{"arrive_time":"17:19","station_name":"无锡东","start_time":"17:21","stopover_time":"2分钟","station_no":"09","isEnabled":true},{"arrive_time":"17:50","station_name":"上海虹桥","start_time":"17:50","stopover_time":"----","station_no":"10","isEnabled":true}]},"messages":[],"validateMessages":{}}'
    class LinkJob(object):
        def __init__(self, task):

            self.task = task
    class TrainTask(object):
        def __init__(self,train_no,train_code):
            self.train_no = train_no
            self.train_code = train_code
    t = TrainTask("240000G1290N","G129")
    l = LinkJob(t)
    ParseStation.parse_content(c,l)