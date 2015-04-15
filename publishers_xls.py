#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import xlwt
from settings import *


row = 1

xls = xlwt.Workbook()
xlsheet = xls.add_sheet('Publishers')

# Setup columns width and title
bold_style = xlwt.XFStyle()
font = xlwt.Font()
font.bold = True
bold_style.font = font

xlsheet.col(0).width = 256 * 36
xlsheet.col(1).width = 256 * 64
xlsheet.col(2).width = 256 * 24
xlsheet.col(3).width = 256 * 36
xlsheet.col(4).width = 256 * 96
xlsheet.col(5).width = 256 * 96

xlsheet.write(0, 0, 'ID', bold_style)
xlsheet.write(0, 1, 'Title', bold_style)
xlsheet.write(0, 2, 'Type', bold_style)
xlsheet.write(0, 3, 'Parent', bold_style)
xlsheet.write(0, 4, 'Homepage', bold_style)
xlsheet.write(0, 5, 'Homepage for spending files', bold_style)

for line in sys.stdin.readlines():
	column = 0

	for value in line.split(CSV_DELIMETER):
		xlsheet.write(row, column, value)
		column += 1
	
	row += 1

xls.save('reports/publishers.xls')