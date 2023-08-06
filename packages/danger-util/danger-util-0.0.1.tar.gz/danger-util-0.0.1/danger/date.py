#-*- coding:utf-8 -*-
'''
strftime(时间转字符串) and strptime(字符串转时间) Format Codes：https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
'''
from datetime import datetime


def get_now(format=None):
	d1 = datetime.now()
	if format is None:
		return d1
	return d1.strftime(format)

def get_weeknum(date_time=None, monday=True):
	if date_time is None:
		date_time=datetime.now()
	if monday:
		return date_time.strftime('%W') #周一开始
	else:
		return date_time.strftime('%U') #周日开始

