#-*- coding:utf-8 -*-
import sys
import os
# import traceback

from datahub import DataHub
# from datahub.exceptions import ResourceExistException
# from datahub.models import FieldType, RecordSchema, TupleRecord, BlobRecord, CursorType, RecordType
ALI_ACCESS_ID =  os.environ.get('ALI_ACCESS_ID', "")
ALI_ACCESS_KEY =  os.environ.get('ALI_ACCESS_KEY', "")


class DataHubHelper(DataHub):
	"""docstring for DataHub
	PS：功能太少，建议使用loghub
	"""
	def __init__(self, access_id = ALI_ACCESS_ID, access_key = ALI_ACCESS_KEY, endpoint = "https://dh-cn-beijing.aliyuncs.com"):
		super(DataHubHelper, self).__init__(access_id, access_key, endpoint)

