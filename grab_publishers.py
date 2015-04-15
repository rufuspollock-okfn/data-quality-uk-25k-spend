#!/usr/bin/python
# -*- coding: utf-8 -*-
import grequests
import math
import re
import requests
from simplejson.scanner import JSONDecodeError
from settings import *


publishers = requests.get(PUBLISHERS_LIST).json()['result']
results = []

# Iterate publishers
for i in range(0, int(math.ceil(float(len(publishers)) / MAX_REQUESTS))):
	for request in grequests.map([
		grequests.get(PUBLISHER_DETAILS % P) for P in publishers[i:(i + 1) * MAX_REQUESTS]
	]):
		try:
			print CSV_DELIMETER.join((lambda **K: [K.get(F, 'NULL') for F in [
				'id',
				'title',
				'category',
				'PARENT', # There is no special field for parent
				'foi-web',
				'HOME-PAGE-FOR-DATA', # There may be multiple pages with files listed on
			]])(**request.json()['result']))

		except AttributeError:
			pass

		except JSONDecodeError:
			pass