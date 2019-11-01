# -*- coding:utf-8 -*-
from util.mysql_util import DataBaseUtil

def compareSS(start,end):
    if start is None:
        start = "0:0"
    s_min = str(start).split(':')
    e_min = str(end).split(':')
    s_int = int(s_min[0])*60+int(s_min[1])
    e_int = int(e_min[0])*60+int(e_min[1])
    duration = e_int-s_int
    return duration*60

def update():
    data = DataBaseUtil.select("select train_code,name,from_name,days,id from train_price_tc where id>114616 and days!=0 ")
    for one in data:
        train_code = one[0]
        name = one[1]
        from_name = one[2]
        days = int(one[3])
        id = one[4]
        if days==0:
            id += 1
            continue
        start_day = 0
        start_arr =DataBaseUtil.select("select  `arrive_time`, `days`, `depart_time` from train_line_stop_tc where train_code ='%s' and name ='%s'" %(train_code,from_name))
        if len(start_arr)!=0:
            start_day = int(start_arr[0][1])
            if compareSS(start_arr[0][0],start_arr[0][2])<0:
                start_day += 1
        end_arr = DataBaseUtil.select("select `days` from train_line_stop_tc where train_code ='%s' and name ='%s'" %(train_code,name))
        end_day = 0
        if len(end_arr)!=0:
            end_day = end_arr[0][0]
        day = end_day -start_day
        if day != days:
            DataBaseUtil.execute("update train_price_tc set days=%s where id =%s" %(day,id))
            print "update %s"% id


if __name__ == '__main__':
    update()