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


# TODO: 先假設要補齊的資料從 2015 開始抓吧
FROM_DATE = '2015-01-01'
# TODO: 先堪用到 2016 年吧！
LAST_DATE = '2016-01-01'

def date_sub(timestr):
    year = int(timestr[:4])
    month = int(timestr[5:7])
    day = int(timestr[8:10])
    return (date(year, month, day) - timedelta(days=1)).strftime('%Y-%m-%d')

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

    ### 從 stocknumber 中讀出看要抓哪幾隻股票的資料
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
            print stock_index, 'exist!'

            lastline = get_last_row(filename)
            print 'lastline = ', lastline
            try:
                st = Share(stock_index+'.tw')
                exact_time = date_sub(st.get_trade_datetime())

                if not time_after(lastline[0], exact_time):
                    print 'time : ', exact_time
                    fo = open(filename, 'ab')
                    cw = csv.writer(fo, delimiter=',')

                    # 更新當天資料
                    cw.writerow([exact_time, st.get_open(), st.get_days_high(),
                                     st.get_days_low(), st.get_price(), st.get_volume(), '0.0'])
                    print "更新一筆！"
                else:
                    print "不需要更新"

            except:
                print stock_index, "update error!"
                error_log_file.write('%s, Update Error\n' % (stock_index))

        # else: # 如果沒有檔案，就從頭開始抓
        #     print stock_index, ' not exist!'
            
        #     try:
        #         st = Share(stock_index+'.tw')
        #         data = st.get_historical('2000-01-01', LAST_DATE)
        #     except:
        #         print stock_index, "create error!"
        #         error_log_file.write('%s, CreateError\n' % (stock_index))
        #         continue

        #     try:
        #         fo = open(join(PATH_OF_DATA, stock_index+'.csv'), 'wb')
        #         cw = csv.writer(fo, delimiter=',')
        #         for i in xrange(len(data)):
        #             datum = data[-(i+1)]
        #             if type(datum) == str:
        #                 print filename, i, "is string"
        #             else:
        #                 cw.writerow([datum['Date'], datum['Open'], datum['High'], datum['Low'], 
        #                              datum['Close'], datum['Volume'], datum['Adj_Close']])
        #     except:
        #         print stock_index, "output error!"
        #         error_log_file.write('%s, OutputError\n' % (stock_index))
        #         continue            



if __name__ == '__main__':
    main()    