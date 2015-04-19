#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import grequests
import math
import re
import requests
import sys
from simplejson.scanner import JSONDecodeError
from settings import *


output = csv.writer(sys.stdout, delimiter=CSV_DELIMETER, quoting=CSV_QUOTING)
publishers = requests.get(PUBLISHERS_LIST).json()['result']
results = {}

# Iterate publishers
for i in range(0, int(math.ceil(float(len(publishers)) / MAX_REQUESTS))):
	for request in grequests.map([
		grequests.get(PUBLISHER_DETAILS % P) for P in publishers[i * MAX_REQUESTS:(i + 1) * MAX_REQUESTS]
	]):
		try:
			publisher = request.json()['result']

			output.writerow([
				publisher['name'],
				publisher['title'],
				publisher.get('category', 'NULL'),
				(publisher.get('groups') or [{}])[0].get('name', 'NULL'),
				PUBLISHER_PAGE % publisher['name'],
			])

		except AttributeError:
			pass

		except JSONDecodeError:
			pass
