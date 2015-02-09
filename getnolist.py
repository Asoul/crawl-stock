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

def main():

    PATH_OF_DATA = 'data'
    error_log_file = open('error.log', 'a')

    index_lists = []
    no_list = []

    ### 從 stocknumber 中讀出看要抓哪幾隻股票的資料
    f = open('stocknumber.csv', 'rb')
    f2 = open('nolist.csv', 'rb')
    for row in csv.reader(f2, delimiter=','):
        no_list.append(row[0])

    cr = csv.reader(f, delimiter=',')
    for row in cr:
        index_lists.append(row[0])

    skipFlag = True if len(sys.argv) > 1 else False
    tillFlag = True if len(sys.argv) > 2 else False
    for stock_index in index_lists:
        if stock_index not in no_list:
            continue
        if skipFlag:
            if stock_index != sys.argv[1]:
                continue
            else:
                skipFlag = False
        if tillFlag:
            if stock_index == sys.argv[2]:
                break

        filename = join(PATH_OF_DATA, stock_index+'.csv')
        print stock_index
        
        try:
            st = Share(stock_index+'.tw')
            data = st.get_historical('2000-01-01', '2100-01-01')
        except:
            print stock_index, "create error!"
            error_log_file.write('%s, CreateError\n' % (stock_index))
            continue

        try:
            fo = open(join(PATH_OF_DATA, stock_index+'.csv'), 'wb')
            cw = csv.writer(fo, delimiter=',')
            for i in xrange(len(data)):
                datum = data[-(i+1)]
                if type(datum) == str:
                    print filename, i, "is string"
                else:
                    cw.writerow([datum['Date'], datum['Open'], datum['High'], datum['Low'], 
                                 datum['Close'], datum['Volume'], datum['Adj_Close']])
        except:
            print stock_index, "output error!"
            error_log_file.write('%s, OutputError\n' % (stock_index))
            continue            


if __name__ == '__main__':
    main()    