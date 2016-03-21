# -*- coding: utf-8 -*-
"""This script preprocesses sources before running spd_admin on them.

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import os
import csv
import fileinput
import sys
import re
import json

# Files path.
FETCHED_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fetched'))
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data'))
INVALID_SOURCE_FILEPATH = os.path.join(DATA_DIR, 'invalid_sources.csv')
LOCAL_SOURCE_FILEPATH = os.path.join(DATA_DIR, 'sources.csv')

def is_empty(datafile):
    """Return true if datafile is an empty file. """
    if os.stat(datafile).st_size == 0:
        return True
    else:
        return False

def has_csv_extension(datafile):
    """Return true if datafile has the extension .csv """
    match = re.search('\.csv$', datafile, re.I)
    if match:
        return True
    else:
        return False

def is_invalid_csv(datafile, encoding='utf-8'):
    """Return true if datafile has too many empty fields in the header. """
    try:
        with open(datafile, mode='r', encoding=encoding) as data:
            reader = csv.DictReader(data)
            fields = reader.fieldnames
            empty_fields = 0
            for field in fields:
                if not field:
                    empty_fields += 1
            if empty_fields > 100:
                return True
            else:
                return False
    except UnicodeDecodeError:
        return is_invalid_csv(datafile, encoding='iso-8859-2')

def is_invalid(datafile):
    """Return true if datafile has NULL bytes in the first line or if it is an html file. """
    with open(datafile, mode='rb') as data:
        for i, l in enumerate(data):
            if i > 100:
                break
            else:
                pass
        row_limit = i
        data.seek(0)

        # Look for NULL bytes in the first line.
        content = data.readline()
        if b'\x00' in content:
            return True
        else:
            # Test if it is an html file.
            for j in range(row_limit):
                content += data.readline()
            html = BeautifulSoup(content, 'html.parser').find()
            if html:
                return True
            else:
                return False

def make_clean_sources(invalid_sources, sources):
    """Make a CSV file with valid sources and another with invalid sources from local_sources CSV file. """

    clean_sources = os.path.join(os.path.dirname(os.path.abspath(sources)), 'clean_surces.csv')
    total_lines = 0
    no_valid_lines = 0

    with open(invalid_sources, mode='w') as invalid:
        fieldnames = ['id', 'publisher_id', 'title', 'data', 'format', 'last_modified', 'period_id', 'schema', 'cache']
        invalid_writer = csv.DictWriter(invalid, fieldnames=fieldnames)
        invalid_writer.writeheader()

        with open(clean_sources, mode='w') as clean:
            clean_writer = csv.DictWriter(clean, fieldnames=fieldnames)
            clean_writer.writeheader()

            with open(sources, mode='r') as source:
                reader = csv.DictReader(source)
                for row in reader:
                    total_lines +=1
                    fetched = row['cache']
                    print('File: ' + fetched)
                    if is_empty(fetched) or is_invalid(fetched) or (has_csv_extension(fetched) and is_invalid_csv(fetched)):
                        invalid_row = row
                        invalid_writer.writerow(invalid_row)
                        print('is invalid')
                    else:
                        clean_row = row
                        clean_writer.writerow(clean_row)
                        no_valid_lines += 1
                        print('is valid')

            os.remove(sources)
            os.rename(clean_sources, sources)

            print("Finished. {0} out of {1} lines are valid.".format(no_valid_lines, total_lines))
