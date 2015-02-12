#!/bin/python
# -*- coding: utf-8 -*-

## 資料格式
# 0. Date
# 1. Open
# 2. High
# 3. Low
# 4. Close
# 5. Volume
# 6. Adj Close*

from yahoo_finance import Share
import csv
import sys
from os.path import join, isfile
from os import listdir
from datetime import date, timedelta

def time_after(timea, timeb):
    if int(timea[:4]) > int(timeb[:4]):
        return True
    elif int(timea[5:7]) > int(timeb[5:7]):
        return True
    elif int(timea[8:10]) > int(timeb[8:10]):
        return True
    elif int(timea[8:10]) == int(timeb[8:10]):
        return True
    else:
        return False

def get_last_row(csv_filename):
    with open(csv_filename,'rb') as f:
        for line in csv.reader(f):
            lastline = line
        return lastline

def main():

    PATH_OF_DATA = 'data'
    error_log_file = open('error.log', 'a')

    index_lists = [ f[:-4] for f in listdir(PATH_OF_DATA) if f[-4:] == '.csv' ]

    skipFlag = True if len(sys.argv) > 1 else False
    tillFlag = True if len(sys.argv) > 2 else False
    for stock_index in index_lists:
        if skipFlag:
            if stock_index != sys.argv[1]:
                continue
            else:
                skipFlag = False
        if tillFlag:
            if stock_index == sys.argv[2]:
                break

        filename = join(PATH_OF_DATA, stock_index+'.csv')
        if isfile(filename):# 如果已經有檔案，就讀出最後一行然後插入在後面
            lastline = get_last_row(filename)
            print 'lastline = ', lastline
            try:
                st = Share(stock_index+'.tw')

                if not time_after(lastline[0], st.get_trade_datetime()[:10]):
                    print 'time : ', st.get_trade_datetime()[:10]
                    fo = open(filename, 'ab')
                    cw = csv.writer(fo, delimiter=',')

                    # 更新當天資料
                    cw.writerow([st.get_trade_datetime()[:10], st.get_open(), st.get_days_high(),
                                     st.get_days_low(), st.get_price(), st.get_volume(), '0.0'])
                    print "更新一筆！"
                else:
                    print "不需要更新"

            except:
                print stock_index, "update error!"
                error_log_file.write('%s, Update Error\n' % (stock_index))

if __name__ == '__main__':
    main()    