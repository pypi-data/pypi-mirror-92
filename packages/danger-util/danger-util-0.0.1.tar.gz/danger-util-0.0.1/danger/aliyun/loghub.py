#-*- coding:utf-8 -*-
import sys
import os

from aliyun.log import LogClient

ALI_ACCESS_ID =  os.environ.get('ALI_ACCESS_ID', "")
ALI_ACCESS_KEY =  os.environ.get('ALI_ACCESS_KEY', "")


class LogHubHelper(LogClient):
    """docstring for LogHub
    """
    def __init__(self, access_id = ALI_ACCESS_ID, access_key = ALI_ACCESS_KEY, endpoint = "cn-beijing.log.aliyuncs.com"):
        super(LogHubHelper, self).__init__(endpoint, access_id, access_key)
