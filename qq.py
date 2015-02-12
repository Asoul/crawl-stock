import csv
from os import listdir
index_lists = [ f[:-4] for f in listdir('data') if f[-4:] == '.csv' ]
for filename in index_lists:
    f = open('data/'+filename+'.csv', 'rb')
    rows = []
    for row in f:
        if row.find('UTC+0000') >= 0:
            old = row
            row = old[:10]+old[28:]
            rows.append(row)
        else:
            rows.append(row)
    f.close()
    f = open('data/'+filename+'.csv', 'wb')
    for row in rows:
        f.write(row)