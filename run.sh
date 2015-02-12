#!/bin/bash

cd /root/crawl-stock/
python crawl.py
git add .
git commit -m "daily update"
git push
