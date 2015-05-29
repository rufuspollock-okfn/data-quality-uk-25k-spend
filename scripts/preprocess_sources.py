# -*- coding: utf-8 -*-
"""This script preprocesses datafiles before running spd_admin on them.

"""

import requests
import os
import csv
import fileinput
import sys
import re
from bs4 import BeautifulSoup
from datetime import datetime
import json

# Files path.
ARCHIVE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'archive'))
CURRENT_DATE = datetime.utcnow().strftime('%Y-%m-%d')
CURRENT_DATE_DIR = ARCHIVE_DIR + '/' + CURRENT_DATE

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data'))
INVALID_SOURCE_FILEPATH = os.path.join(DATA_DIR, 'invalid_datafiles.csv')
LOCAL_SOURCE_FILEPATH = os.path.join(DATA_DIR, 'local_datafiles.csv')
CLEAN_SOURCE_FILEPATH = os.path.join(DATA_DIR, 'clean_datafiles.csv')

LOCALHOST = 'http://localhost:8000'
RELATIVE_DATE_DIR = LOCALHOST + '/archive/' + CURRENT_DATE + '/'

def get_filpath(local_url):
    """Return file path from local url. """
    file_name = re.sub(RELATIVE_DATE_DIR, '', local_url)
    filepath = ARCHIVE_DIR + '/' + CURRENT_DATE + '/' + file_name
    return filepath

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

def make_clean_sources(invalid_sources, local_sources, clean_sources):
    """Make a CSV file with valid sources and another with invalid sources from local_sources CSV file. """
    with open(invalid_sources, mode='w') as invalid:
        fieldnames = ['id', 'publisher_id', 'title', 'data', 'format', 'last_modified', 'period_id', 'schema']
        invalid_writer = csv.DictWriter(invalid, fieldnames=fieldnames)
        invalid_writer.writeheader()

        with open(clean_sources, mode='w') as clean:
            clean_writer = csv.DictWriter(clean, fieldnames=fieldnames)
            clean_writer.writeheader()

            with open(local_sources, mode='r') as local:
                reader = csv.DictReader(local)
                for row in reader:
                    filepath = get_filpath(row['data'])
                    print('File: ' + filepath)
                    if is_empty(filepath) or is_invalid(filepath) or (has_csv_extension(filepath) and is_invalid_csv(filepath)):
                        invalid_row = row
                        invalid_writer.writerow(invalid_row)
                        print('is invalid')
                    else:
                        clean_row = row
                        clean_writer.writerow(clean_row)
                        print('is valid')



# Make a CSV file with valid sources and another with invalid sources from local_sources.csv.
make_clean_sources(INVALID_SOURCE_FILEPATH, LOCAL_SOURCE_FILEPATH, CLEAN_SOURCE_FILEPATH)
