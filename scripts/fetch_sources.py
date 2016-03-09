# -*- coding: utf-8 -*-
"""This script fetches spending data files.

"""

import requests
import csv
import time
from datetime import datetime
import re
import os

# Prepare directories and paths.
# Make archive directory
MAIN_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
try:
    os.mkdir(MAIN_DIR + '/archive')
except OSError as e:
    pass
ARCHIVE_DIR = MAIN_DIR + '/archive'

# Make current date subdirectory
CURRENT_DATE = datetime.utcnow().strftime('%Y-%m-%d')
try:
    os.mkdir(ARCHIVE_DIR + '/' + CURRENT_DATE)
except OSError as e:
    pass
CURRENT_DATE_DIR = ARCHIVE_DIR + '/' + CURRENT_DATE

# Sources file path.
SOURCES_FILEPATH = os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')), 'sources.csv')


def fetch_file(url):
    """Return fetched file from url. """

    print('Get: ' + url)
    response_content = bytes()
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('Error: ' + str(e))
    except requests.exceptions.ConnectionError as e:
        print('Error: ' + str(e))
    except requests.exceptions.RequestException as e:
        print('Error: ' + str(e))
    else:
        response_content = response.iter_content(chunk_size=1024)
    return response_content

def make_archive_file(content, file_id, file_url):
    """Create a file in archive directory.

    Parameters:
    content (bytes): content of the file
    file_id (str): file id used as file name in archive
    file_url (str): url of the file

    """

    filepath = CURRENT_DATE_DIR + '/' + file_id
    match = re.search('\.[a-z]{3,4}$', file_url, re.I)
    if match:
        filepath += match.group(0)
    with open(filepath, mode='wb') as data:
        for chunk in content:
            if chunk:
                data.write(chunk)
                data.flush()
    print('Path: ' + filepath)

def make_archive(sources):
    """Fetch all data files from sources and store them in archive directory.

    Parameter:
    sources (str): file path of CSV file with all data files

    """

    with open(sources, mode='r') as data:
        reader = csv.DictReader(data)
        for row in reader:
            content = fetch_file(row['data'])
            # Wait to avoid traffic control.
            time.sleep(0.6)
            make_archive_file(content, row['id'], row['data'])

# Fetch all files and store them in archive directory
make_archive(SOURCES_FILEPATH)
