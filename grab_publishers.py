#!/usr/bin/python
# -*- coding: utf-8 -*-
import grequests
import math
import re
import requests
from simplejson.scanner import JSONDecodeError
from settings import *


publishers = requests.get(PUBLISHERS_LIST).json()['result']
results = {}

# Iterate publishers
for i in range(0, int(math.ceil(float(len(publishers)) / MAX_REQUESTS))):
	for request in grequests.map([
		grequests.get(PUBLISHER_DETAILS % P) for P in publishers[i * MAX_REQUESTS:(i + 1) * MAX_REQUESTS]
	]):
		try:
			publisher = request.json()['result']

			# Manage parent records
			results[publisher['name']] = [
				publisher['id'],
				publisher['name'],
				publisher['title'],
				publisher.get('category', 'NULL'),
				(publisher.get('groups') or [{}])[0].get('name', 'NULL'),
				publisher.get('foi-web', 'NULL'),
				PUBLISHER_DATA_PAGE % publisher['name'], # There may be multiple pages with files listed on
			]

			print CSV_DELIMETER.join(results[publisher['name']])

		except AttributeError:
			pass

		except JSONDecodeError:
			pass
