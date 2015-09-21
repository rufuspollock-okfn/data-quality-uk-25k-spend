# -*- coding: utf-8 -*-
"""This script makes a new CSV sources file with local urls.

"""

import os
from datetime import datetime
import csv
import re

# Settings
# Files path.
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data'))
SOURCE_FILEPATH = os.path.join(DATA_DIR, 'sources.csv')
LOCAL_SOURCE_FILEPATH = os.path.join(DATA_DIR, 'local_sources.csv')

MAIN_DIR = (os.path.dirname(os.path.dirname(__file__)))
ARCHIVE_DIR = MAIN_DIR + '/archive'
CURRENT_DATE = datetime.utcnow().strftime('%Y-%m-%d')
CURRENT_DATE_DIR = ARCHIVE_DIR + '/' + CURRENT_DATE

def get_url(source_id, source_url):
    """Return local url of a file. """

    filepath = CURRENT_DATE_DIR + '/' + source_id
    match = re.search('\.[a-z]{3,4}$', source_url, re.I)
    if match:
        filepath += match.group(0)
    url = 'http://localhost:8000' + filepath
    return url

def make_local_sources(sources, local_sources):
    """Make a sources CSV file with local urls. """

    with open(local_sources, mode='w') as local:
        fieldnames = ['id', 'publisher_id', 'title', 'data', 'format', 'last_modified', 'period_id', 'schema']
        writer = csv.DictWriter(local, fieldnames=fieldnames)
        writer.writeheader()

        with open(sources, mode='r') as data:
            reader = csv.DictReader(data)
            for row in reader:
                localrow = row
                localrow['data'] = get_url(row['id'], row['data'])
                writer.writerow(localrow)

# Make a sources CSV file with local urls.
make_local_sources(SOURCE_FILEPATH, LOCAL_SOURCE_FILEPATH)