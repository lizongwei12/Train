#-*- coding: utf-8 -*-
import sys
sys.path.append("..")
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
import json
import codecs
from data_service import DataService
import date_util
import traceback
import logging as log
from settings import check_heades
import mycurl
import time

def get_price(key,dic):
    p = 0
    if  len(dic)==0:
        return p
    if key in dic:
        p = dic[key]['price']
    return p

def create_url(detail):
    millis = int(round(time.time() * 1000))
    callback = "jQuery18309102298273607763_%s" % millis
    para ={"To":detail['end_stop'],"From":detail['begin_stop'],"TrainDate":detail['fetched_date'],"PassType":"","TrainClass":"","FromTimeSlot":"","ToTimeSlot":"","FromStation":"","ToStation":"","SortBy":"fromTime","callback":"","tag":"","memberId":"0","headct":"0","platId":1,"headver":"1.0.0","headtime":int(round(time.time() * 1000))}
    para=json.dumps(para)
    url = "https://www.ly.com/uniontrain/trainapi/TrainPCCommon/SearchTrainRemainderTickets?callback=%s&para=%s"
    url = url % (callback,para)
    return url

class PrasePrice(object):

    def __init__(self):
        pass

    @classmethod
    def if_has_data(self,content):
        if content:
            try:
                content = content[content.index('(')+1:content.rindex(')')]
                json_obj = json.loads(content)
                if len(json_obj['data']["trains"]) != 0:
                    return True
            except:
                pass
        return False

    @classmethod
    def parse_content(self,content,link_job):
        content = content[content.index('(')+1:content.rindex(')')]
        json_obj = json.loads(content)
        trains = json_obj['data']['trains']
        for train in trains:
            try:
                train_code = train['trainNum']
                start_station = train['fromCity']
                end_station = train['toCity']
                origin = train['beginPlace']
                terminal = train['endPlace']
                depart_time = train['fromTime']
                arrive_time = train['toTime']
                duration = int(train['usedTimeInt'])*60
                note = train['note']
                A1 = get_price('hardseat',train['ticketState'])
                A2 = get_price('softseat',train['ticketState'])
                A3 = get_price('hardsleepermid',train['ticketState'])
                A4 = get_price('softsleeperdown',train['ticketState'])
                A6 = get_price('advancedsoftsleeper',train['ticketState'])
                A9 = get_price('businessseat',train['ticketState'])
                O = get_price('secondseat',train['ticketState'])
                M = get_price('firstseat',train['ticketState'])
                P = get_price('specialseat',train['ticketState'])
                sequence = 0
                days = 0
                stayTime = 0
                grade = ''
                state = 0
                train_no = ''
                exist = DataService.check_traincode_exist(train_code)
                # is_correct 0：错误信息 1:正确
                is_correct = 1
                if len(train['ticketState']) ==0:
                    is_correct = 0
                #  state 0：正常   1：未收录此车次    2:收录此车次但是此站点已经取消
                if not exist:
                    state =1
                else:
                    station_s = DataService.find_station(train_code,start_station)
                    station_e = DataService.find_station(train_code,end_station)
                    if len(station_e) != 0 and len(station_s)!=0:
                        days_s = int(station_s[0][6])
                        if date_util.compareSS(station_s[0][4],station_s[0][8])<0:
                            days_s += 1
                        sequence = station_e[0][3]
                        days = station_e[0][6] - days_s
                        stayTime = station_e[0][5]
                        grade = station_e[0][9]
                        train_no = station_e[0][10]
                    else:
                        state =2
                price = Price(train_code,end_station,start_station,depart_time,arrive_time,duration,A1,A2,A3,A4,O,M,A6,A9,grade,days,P,origin,terminal,sequence,train_no,stayTime,is_correct,state,note)
                DataService.save_train_price(price)
            except:
                t, v, tb = sys.exc_info()
                log.error("%s,%s,%s" % (t, v, traceback.format_tb(tb)))

    @classmethod
    def check_proxy_available(cls,ip, port):
        flag = False
        try:
            detail = {"end_stop":"广州","begin_stop":"哈尔滨东","fetched_date":"2017-07-14"}
            check_url = create_url(detail)
            response = mycurl.get(check_url,request_headers=check_heades,timeout=5, proxy="%s:%s" % (ip,port))
            if response.status == 200:
                content = response.body
                if content:
                    content = content[content.index('(')+1:content.rindex(')')]
                    json_obj = json.loads(content)
                    if json_obj["status"]==200:
                        flag = True
        except:
            pass
        return flag

class Price(object):
    def __init__(self,train_code,end_station,start_station,depart_time,arrive_time,duration,A1,A2,A3,A4,O,M,A6,A9,grade,days,P,origin,terminal,sequence,train_no,stayTime,is_correct,state,note):
        self.train_code = train_code
        self.end_station = end_station
        self.start_station = start_station
        self.depart_time = depart_time
        self.arrive_time = arrive_time
        self.duration = duration
        self.A1 = A1
        self.A2 = A2
        self.A3 = A3
        self.A4 = A4
        self.O = O
        self.M = M
        self.A6 = A6
        self.A9 = A9
        self.grade = grade
        self.days = days
        self.P = P
        self.origin = origin
        self.terminal = terminal
        self.sequence = sequence
        self.train_no = train_no
        self.stayTime = stayTime
        self.is_correct = is_correct
        self.state =  state
        self.note = note

if __name__ == '__main__':
    w = codecs.open('E:/price.json','r','gb2312')
    content = w.read()
    json_obj = content[content.index('(')+1:content.rindex(')')]
    json_obj = json.loads(json_obj)
    # PrasePrice.parse_price_content(json_obj)

