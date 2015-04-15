#!/usr/bin/python
# -*- coding: utf-8 -*-
import grequests
import math
import re
import requests
import sys
from settings import *
from simplejson.scanner import JSONDecodeError


publishers = [P.split(CSV_DELIMETER) for P in sys.stdin.readlines()]

# Iterate publishers
for i in range(0, int(math.ceil(float(len(publishers)) / MAX_REQUESTS))):
	for request in grequests.map([
		grequests.get(PUBLISHER_DETAILS % P[0]) for P in publishers[i * MAX_REQUESTS:(i + 1) * MAX_REQUESTS]
	]):
		try:
			# Iterate appropriate packages
			for package in request.json()['result']['packages']:
				# Spend amount may be specified both in title and name
				S = package['name'] + package['title']

				if not re.findall('(spend|spent|expenditure)', S, re.I):
					continue

				if not re.findall('(500|25000|25 000|25,000|25K)[\s\.\,]+', S, re.I):
					continue

				spend_over = 500

				if re.findall('(25000|25 000|25,000|25K)[\s\.\,]+', S, re.I):
					spend_over = 25000

				# Now get links to all resources belong to package
				for resource in requests.get(PACKAGE_FILES % package['id']).json()['result'].get('resources'):
					try:
						if resource['resource_type'] != 'file':
							continue

						print CSV_DELIMETER.join([
							resource['id'],
							resource['url'],
							resource['description'],
							resource.get('mimetype', 'NULL'),
							resource['hash'],
							request.url.split('?id=')[1],
							'NULL',
							str(spend_over)
						])
						
					except KeyError:
						pass
						
					except UnicodeEncodeError:
						pass

		except AttributeError:
			pass

		except JSONDecodeError:
			pass

		except KeyError:
			pass
