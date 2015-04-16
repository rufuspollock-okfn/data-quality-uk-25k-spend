#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import sqlite3
import sys
from settings import *
from optparse import OptionParser


output = csv.writer(sys.stdout, delimiter=CSV_DELIMETER, quoting=CSV_QUOTING)

parser = OptionParser()
parser.add_option('-t', '--table', dest='table', help='DB table to be extracted')
parser.add_option('-o', '--orderby', dest='orderby', help='Order output by field')

(options, args) = parser.parse_args()

db = sqlite3.connect(DB_NAME)
cursor = db.cursor()

cursor.execute('pragma table_info(%s)' % options.table)
output.writerow(map(lambda C: C[1], cursor.fetchall()))

cursor.execute('select * from %s%s' % (
	options.table,
	options.orderby and ' order by %s' % options.orderby or ''
))

for row in cursor.fetchall():
	output.writerow([(C and str(C).strip()) or 'NULL' for C in row])

db.close()