#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Derived from the code of original author: Rohan Achar ra.rohan@gmail.com
'''

from Crawler4py.Crawler import Crawler
from MyConfig import MyConfig

crawler = Crawler(MyConfig())

print (crawler.StartCrawling())

exit(0)
