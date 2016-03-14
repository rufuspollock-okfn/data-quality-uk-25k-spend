# -*- coding: utf-8 -*-
"""This script fetches spending data files.

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import csv
import time
import re
import os
import shutil

from preprocess_sources import make_clean_sources

# Prepare directories and paths.
MAIN_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Sources file path.
SOURCES_FILEPATH = os.path.join(os.path.abspath(os.path.join(MAIN_DIR, 'data')), 'sources.csv')
INVALID_FILEPATH = os.path.join(os.path.abspath(os.path.join(MAIN_DIR, 'data')), 'invalid_sources.csv')

def clean_fetched_dir():
    """ Set up the /fetched directory """

    fetched_dir_path = MAIN_DIR + '/fetched'
    # If the directory /fetched exists, clear it
    if os.path.lexists(fetched_dir_path):
        for filename in os.listdir(fetched_dir_path):
            file_path = os.path.join(fetched_dir_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print('Error: ' + str(e))
    # Otherwise, make it
    else:
        os.mkdir(fetched_dir_path)

    return fetched_dir_path

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

def make_cache_file(content, file_id, file_url, dir_name):
    """Create a file in fetched directory.

    Parameters:
    content (bytes): content of the file
    file_id (str): file id used as file name in archive
    file_url (str): url of the file

    """

    filepath = os.path.join(dir_name, file_id)
    match = re.search('\.[a-z]{3,4}$', file_url, re.I)
    if match:
        filepath += match.group(0)
    with open(filepath, mode='wb') as data:
        for chunk in content:
            if chunk:
                data.write(chunk)
                data.flush()

    print('Path: ' + filepath)
    return filepath


def make_cache(sources):
    """Fetch all data files from sources, store them in /fetched directory and
        add the cached file path to sources.csv cache column

    Parameter:
    sources (str): file path of CSV file with all data files

    """
    fetch_path = clean_fetched_dir()
    temp_file = os.path.join(os.path.dirname(os.path.abspath(sources)), 'temp_surces.csv')
    with open(sources, mode='r') as indata:
        with open(temp_file, mode='w+t', encoding='utf-8') as outdata:
            reader = csv.DictReader(indata)
            output_headers = ['id', 'publisher_id', 'title', 'data', 'format',
                            'last_modified', 'period_id', 'schema', 'cache']
            writer = csv.DictWriter(outdata, output_headers)
            writer.writeheader()

            for row in reader:
                content = fetch_file(row['data'])
                # Wait to avoid traffic control.
                time.sleep(0.6)
                cache_path = make_cache_file(content, row['id'], row['data'], fetch_path)
                row['cache'] = cache_path
                writer.writerow(row)

    os.remove(sources)
    os.rename(temp_file, sources)

# Fetch all files and store them in archive directory
make_cache(SOURCES_FILEPATH)
make_clean_sources(INVALID_FILEPATH, SOURCES_FILEPATH)
