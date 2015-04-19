#!/usr/bin/python
# -*- coding: utf-8 -*-
import grequests
import math
import re
import requests
import sys
from settings import *
from simplejson.scanner import JSONDecodeError


# Use passed connections list to get list files from connections URLs
def grab_files(connections):
	# Keep track of loop index
	i = 0

	for request in grequests.map([C[1] for C in connections]):
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

						output.writerow([
							resource['id'],
							resource['url'],
							DATASET_PAGE % package['name'],
							resource['description'],
							resource.get('mimetype', 'NULL'),
							resource.get('format', 'NULL'),
							resource['hash'],
							connections[i][0],
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

	i += 1


publishers = csv.reader(sys.stdin.readlines(), delimiter=CSV_DELIMETER, quoting=CSV_QUOTING)
output = csv.writer(sys.stdout, delimiter=CSV_DELIMETER, quoting=CSV_QUOTING)
requests_pull = []

for publisher in publishers:
	# Fill up async connections pull
	requests_pull.append([publisher[0], grequests.get(PUBLISHER_DETAILS % publisher[0])])

	if len(requests_pull) < MAX_REQUESTS:
		continue

	grab_files(requests_pull)
	last_publisher = publisher
	requests_pull = []

# There may be < MAX_REQUESTS connections in requests_pull
grab_files(requests_pull)