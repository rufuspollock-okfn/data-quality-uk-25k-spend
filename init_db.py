#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
from settings import *


db = sqlite3.connect(DB_NAME)

db.execute('''CREATE TABLE publisher(
	id CHAR(32) PRIMARY KEY,
	title CHAR(255),
	type CHAR(64),
	parent CHAR(96),
	homepage CHAR(255),
	"homepage-for-data" CHAR(255)
)''')

db.execute('''CREATE TABLE datafile(
	id CHAR(32) PRIMARY KEY,
	url CHAR(255),
	title CHAR(255),
	mediatype CHAR(128),
	format CHAR(32),
	hash CHAR(255),
	publisher CHAR(128),
	period CHAR(32),
	"spend-over" INT
)''')

print '\033[92mDB %s create!\033[0m' % DB_NAME