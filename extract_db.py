#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
from settings import *
from optparse import OptionParser


parser = OptionParser()
parser.add_option('-t', '--table', dest='table', help='DB table to be extracted')
parser.add_option('-o', '--orderby', dest='orderby', help='Order output by field')

(options, args) = parser.parse_args()

db = sqlite3.connect(DB_NAME)
cursor = db.cursor()

cursor.execute('pragma table_info(%s)' % options.table)

print CSV_DELIMETER.join(map(lambda C: C[1], cursor.fetchall()))

cursor.execute('select * from %s%s' % (
	options.table,
	options.orderby and ' order by %s' % options.orderby or ''
))

print '\n'.join([CSV_DELIMETER.join([F and str(F).strip() or 'NULL' for F in P]) for P in cursor.fetchall()])

db.close()