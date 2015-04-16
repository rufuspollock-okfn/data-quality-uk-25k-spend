#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import sqlite3
from settings import *
from optparse import OptionParser


parser = OptionParser()
parser.add_option('-t', '--table', dest='table', help='DB table to be updated with new records')
(options, args) = parser.parse_args()

db = sqlite3.connect(DB_NAME)
success_count = 0
unique_count = 0

for row in csv.reader(sys.stdin.readlines(), delimiter=CSV_DELIMETER, quoting=CSV_QUOTING):
	if not row:
		continue

	try:
		db.cursor().execute('INSERT INTO %s VALUES (%s)' % (options.table, ', '.join([
			R == 'NULL' and R or '"%s"' % R for R in row
		])))

		success_count += 1

	except sqlite3.IntegrityError:
		unique_count += 1

	except sqlite3.OperationalError:
		pass

db.commit()
db.close()

if success_count:
	print '\033[92m%d records successfully inserted\033[0m' % success_count

if unique_count:
	print '\033[93m%d non unique id\033[0m' % unique_count