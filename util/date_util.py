# -*- coding:utf-8 -*-
import datetime
import time
def increaseDate(dateStr,day=1):
    try:
        d = datetime.datetime.strptime(dateStr,'%Y-%m-%d')
        delta=datetime.timedelta(days=day)
        n_days=d+delta
        tDate = n_days.strftime('%Y-%m-%d')
        return tDate
    except Exception ,e:
        print e
    return time.strftime('%Y-%m-%d', time.localtime(time.time()))

def compareSS(start,end):
    if start is None:
        start = "0:0"
    if end is None:
        end = "0:0"
    s_min = str(start).split(':')
    e_min = str(end).split(':')
    s_int = int(s_min[0])*60+int(s_min[1])
    e_int = int(e_min[0])*60+int(e_min[1])
    duration = e_int-s_int
    return duration*60

if __name__ == '__main__':
    print increaseDate('d17-04-30')