# -*- coding:utf-8 -*-
import re
import time
from util.data_service import DataService
from util.prase_station_12306 import TrainStop
import logging as log
import logger
class MergeTrain:

    def __init__(self):
        pass

    # one step :init train_merge_code table
    @classmethod
    def start_merge(cls):
        code_dict = {}
        rmv_zero = r'^(0+)'
        stop_no = DataService.get_stop_no()
        for stop in stop_no:
            train_code = stop[0]
            train_no = stop[1]
            substring_str = re.sub(rmv_zero,"",train_no[2:len(train_no)-2])
            DataService.insert_merge_stop(train_code,train_no,substring_str)
            log.info("insert:%s,%s,%s" % (train_code,train_no,substring_str))
            if substring_str in code_dict:
                temp_code = code_dict[substring_str]
                temp_code = "%s/%s" %(temp_code,train_code)
                code_dict[substring_str] = temp_code
            else:
                code_dict[substring_str] = train_code
        for sub_str in code_dict:
            DataService.update_merge_stop(code_dict[sub_str],sub_str)

    # two step :add merge stop
    @classmethod
    def add_merge_train_code(cls):
        merge_codes = DataService.select_merge_codes()
        for item in merge_codes:
            train_code = item[0]
            merge_code = item[1]
            # exist = DataService.check_traincode_exist(merge_code)
            # if exist:
            #     continue
            stops = DataService.get_stops(train_code)
            log.info("insert merge_train_stop：%s" % merge_code)
            for stop in stops:
                train_stop = TrainStop(merge_code,stop[2],stop[3],stop[4],stop[5],stop[6],stop[7],stop[8],stop[9],stop[10])
                DataService.save_train_stop(train_stop)


    # three step :update price
    @classmethod
    def update_price_code(cls):
        merge_codes = DataService.select_merge_codes()
        for item in merge_codes:
            train_code = item[0]
            merge_code = item[1]
            log.info('update price code ,%s,%s'% (train_code,merge_code))
            DataService.update_price_code(merge_code,train_code)


if __name__ == '__main__':
    log.info('start merge:___________')
    # MergeTrain.start_merge()
    # MergeTrain.add_merge_train_code()
    MergeTrain.update_price_code()