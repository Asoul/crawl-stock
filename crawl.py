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


# TODO: 先假設要補齊的資料從 2015 開始抓吧
FROM_DATE = '2015-01-01'
# TODO: 先堪用到 2016 年吧！
LAST_DATE = '2016-01-01'

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

            lastline = get_last_row(filename)
            print 'lastline = ', lastline
            try:
                st = Share(stock_index+'.tw')
                
                if lastline[0] != st.get_trade_datetime()[:10]:#如果需要更新的話
                    
                    fo = open(filename, 'ab')
                    cw = csv.writer(fo, delimiter=',')

                    # 先假設每天抓，好像historical有錯

                    # data = st.get_historical(FROM_DATE, LAST_DATE)# 先堪用到年底


                    # # 先更新歷史資料
                    # startDate = lastline[0]
                    # startFlag = False
                    # for i in xrange(len(data)):
                    #     datum = data[-(i+1)]
                    #     if datum['Date'] == lastline[0]:
                    #         startFlag = True
                    #         continue
                    #     if startFlag:
                    #         startFlag = False
                    #     else:
                    #         continue
                    #     # 先不抓 adj close 吧！
                    #     cw.writerow([datum['Date'], datum['Open'], datum['High'], datum['Low'], 
                    #                      datum['Close'], datum['Volume'], datum['Adj_Close']])

                    # 再更新當天資料
                    cw.writerow([st.get_trade_datetime()[:10], st.get_open(), st.get_days_high(),
                                     st.get_days_low(), st.get_price(), st.get_volume(), '0.0'])

            except:
                print stock_index, "update error!"
                error_log_file.write('%s' % (stock_index))

        else: # 如果沒有檔案，就從頭開始抓
            print stock_index, ' not exist!'
            
            try:
                st = Share(stock_index+'.tw')
                data = st.get_historical('2000-01-01', LAST_DATE)
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