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

def get_last_row(csv_filename):
    with open(csv_filename,'rb') as f:
        for line in csv.reader(f):
            lastline = line
        return lastline

def main():

    PATH_OF_DATA = 'data'
    error_log_file = open('error.log', 'a')

    index_lists = []

    ### 從 stocknumber 中讀出看要抓哪幾隻股票的資料
    f = open('stocknumber.csv', 'rb')
    cr = csv.reader(f, delimiter=',')
    for row in cr:
        index_lists.append(row[0])

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

            # lastline = get_last_row(filename)
            # try:
            #     st = Share(stock_index+'.tw')
            #     infos = st.get_info()
            #     data = st.get_historical('2015-01-01', infos['end'])
                
            #     fo = open(filename, 'ab')
            #     cw = csv.writer(fo, delimiter=',')

            #     startFlag = False
            #     for i in xrange(len(data)):
            #         datum = data[-(i+1)]
            #         if not startFlag:
            #             if datum['Date'] == lastline[0]:
            #                 startFlag = True
            #                 count = 0
            #         else:
            #             count += 1
            #             cw.writerow([datum['Date'], datum['Open'], datum['High'], datum['Low'],
            #                          datum['Close'], datum['Volume'], datum['Adj_Close']])                    

            #     print "差了 "+str(count)+" 筆資料"

            # except:
            #     print stock_index, "error!"
            #     error_log_file.write('%d' % (stock_index))

        else: # 如果沒有檔案，就從頭開始抓
            print stock_index, ' not exist!'
            
            try:
                st = Share(stock_index+'.tw')
                infos = st.get_info()
                data = st.get_historical(infos["start"], infos["end"])
                
                fo = open(join(PATH_OF_DATA, stock_index+'.csv'), 'wb')
                cw = csv.writer(fo, delimiter=',')
                for i in xrange(len(data)):
                    cw.writerow([data[-(i+1)]['Date'], data[-(i+1)]['Open'], data[-(i+1)]['High'],
                                data[-(i+1)]['Low'], data[-(i+1)]['Close'], data[-(i+1)]['Volume'],
                                data[-(i+1)]['Adj_Close']])
            except:
                print stock_index, "error!"
                error_log_file.write('%d' % (stock_index))


if __name__ == '__main__':
    main()    