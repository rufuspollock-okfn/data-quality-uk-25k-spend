#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import sys
import xlwt
from settings import *


publishers = {}
row = 1

db = sqlite3.connect(DB_NAME)
cursor = db.cursor()

xls = xlwt.Workbook()
xlsheet = xls.add_sheet('Datafiles')

# Setup columns width and title
bold_style = xlwt.XFStyle()
font = xlwt.Font()
font.bold = True
bold_style.font = font

xlsheet.col(0).width = 256 * 36
xlsheet.col(1).width = 256 * 96
xlsheet.col(2).width = 256 * 96
xlsheet.col(3).width = 256 * 16
xlsheet.col(4).width = 256 * 48
xlsheet.col(5).width = 256 * 64
xlsheet.col(6).width = 256 * 16
xlsheet.col(7).width = 256 * 16

xlsheet.write(0, 0, 'ID', bold_style)
xlsheet.write(0, 1, 'URL', bold_style)
xlsheet.write(0, 2, 'Title', bold_style)
xlsheet.write(0, 3, 'Mime-type', bold_style)
xlsheet.write(0, 4, 'Hash', bold_style)
xlsheet.write(0, 5, 'Publisher', bold_style)
xlsheet.write(0, 6, 'Period', bold_style)
xlsheet.write(0, 7, 'Spend over', bold_style)

# Group input files by publisher
for line in sys.stdin.readlines():
	values = line.split(CSV_DELIMETER)

	try:
		publishers.setdefault(values[5], []).append(values)
	except IndexError:
		pass

cursor.execute('select * from publisher')

for publisher in cursor.fetchall():
	xlsheet.write(row, 0, publisher[2], bold_style)
	row += 1

	for datafile in publishers.get(publisher[0], [['N/A']]):
		column  = 0

		for value in datafile:
			xlsheet.write(row, column, value.rstrip())
			column += 1

		row += 1

xls.save('reports/datafiles.xls')
db.close()