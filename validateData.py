#!/bin/python
# -*- coding: utf-8 -*-

import csv
import sys
from os.path import join, isfile
from os import listdir
import os

def main():
    
    DATA_PATH = 'data'
    file_list = [ f for f in listdir(DATA_PATH) if f[-4:] == '.csv' ]

    # 看有沒有內容
    # print "Validate have contents"
    for filename in file_list:
        fin = open(join(DATA_PATH, filename), 'rb')
        count = 0
        for row in csv.reader(fin, delimiter=","):
            count += 1
        if count == 0:
            print filename, " no data"

    # # 看每一個檔案中有沒有重複的天數
    # print "Validate conflict data..."
    # for filename in file_list:
    #     fin = open(join(DATA_PATH, filename), 'rb')
    #     dates = set()
    #     for row in csv.reader(fin, delimiter=","):
    #         if row[0] in dates:
    #             print '[CONFLICT]', filename, row
    #         else:
    #             dates.add(row[0])

    # 看檔案中有沒有奇怪的資料（一行不是 7 段的），就移除掉
    # print "Validate strange data then rewrite all data again"
    # for filename in file_list:
    #     fin = open(join(DATA_PATH, filename), 'rb')
    #     rows = []
    #     errorFlag = False
    #     for row in csv.reader(fin, delimiter=","):
    #         if len(row) == 7:
    #             rows.append(row)
    #         else:
    #             errorFlag = True
    #     if errorFlag:
    #         print '[STRANGE]', filename
    #         fout = open(join(DATA_PATH, filename), 'wb')
    #         cw = csv.writer(fout, delimiter=',')
    #         for row in rows:
    #             cw.writerow(row)

    # 把現在不能買的刪掉
    # for filename in file_list:
    #     fin = open(join(DATA_PATH, filename), 'rb')
    #     for row in csv.reader(fin, delimiter=","):
    #         last = row
    #     if last[0] != '2015-02-06':
    #         print '[Not today]', filename
            # os.remove(join(DATA_PATH, filename))

    # 看有沒有跳月跳年的
    # print "Validate missing month and year..."
    # startFlag = True if len(sys.argv) > 1 else False
    # for filename in file_list:
    #     if startFlag:
    #         if filename == (sys.argv[1]+'.csv'):
    #             startFlag = False
    #         else:
    #             continue
    #     fin = open(join(DATA_PATH, filename), 'rb')
    #     firstFlag = True
    #     for row in csv.reader(fin, delimiter=","):
    #         if firstFlag:
    #             year = int(row[0].split('-')[0])
    #             month = int(row[0].split('-')[1])
    #             firstFlag = False
    #             continue

    #         newyear = int(row[0].split('-')[0])
    #         newmonth = int(row[0].split('-')[1])

    #         if newyear > year + 1:
    #             print "[YEAR]", filename, row
    #         if newyear == year and newmonth > month + 1:
    #             print "[MONTH]", filename, row

    #         year = newyear
    #         month = newmonth

    # 看有沒有差超過 7% 的
    # print "Validate missing month and year..."
    # startFlag = True if len(sys.argv) > 1 else False
    # for filename in file_list:
    #     if startFlag:
    #         if filename == (sys.argv[1]+'.csv'):
    #             startFlag = False
    #         else:
    #             continue
    #     fin = open(join(DATA_PATH, filename), 'rb')
    #     firstFlag = True
    #     for row in csv.reader(fin, delimiter=","):
    #         if firstFlag:
    #             year = int(row[0].split('-')[0])
    #             month = int(row[0].split('-')[1])
    #             firstFlag = False
    #             continue

    #         newyear = int(row[0].split('-')[0])
    #         newmonth = int(row[0].split('-')[1])

    #         if newyear > year + 1:
    #             print "[YEAR]", filename, row
    #         if newyear == year and newmonth > month + 1:
    #             print "[MONTH]", filename, row

    #         year = newyear
    #         month = newmonth
            
if __name__ == '__main__':
    main()    