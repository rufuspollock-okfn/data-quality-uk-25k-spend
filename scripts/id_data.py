# -*- coding: utf-8 -*-
"""This script scrapes ministerial departments spending data from http://data.gov.uk/.

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import requests
import json
import sys
import csv
import math
import time
import re
import sys
import os


# Settings
# Files path.
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data'))
PUBLISHER_FILEPATH = os.path.join(DATA_DIR, 'publishers.csv')
SOURCE_FILEPATH = os.path.join(DATA_DIR, 'sources.csv')

# Schema for spending files.
SCHEMA = 'https://cdn.rawgit.com/frictionlessdata/goodtables-py/v1.0.0-alpha8/data/hmt/spend-publishing-schema.json'

def import_dataset(url):
    """Return CKAN dataset.

    Parameters:
    url (str): url of the dataset

    """
    print('Get: ' + url)
    try:
        # Make the HTTP request.
        response = requests.get(url)
        response.raise_for_status()
        assert response.status_code == 200
    except requests.exceptions.HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error: ' + str(e))
        sys.exit(0)
    except requests.exceptions.ConnectionError as e:
        print('Failed to reach the server.')
        print('Error: ' + str(e))
        sys.exit(0)
    except requests.exceptions.RequestException as e:
        print('Error: ' + str(e))
        sys.exit(0)
    except AssertionError:
        print('Unexpected response code from the server.')
        print('Response code: ' + str(response.status_code))
        sys.exit(0)
    else:
        try:
            # Load CKAN's response into a dictionary.
            response_dict = response.json()
        except ValueError:
            print('JSON response content decoding failed.')
            sys.exit(0)
        else:
            try:
                # Check the content of the response.
                assert response_dict.get('success') is True
            except AssertionError:
                print('API request failed.')
                sys.exit(0)
            else:
                result = response_dict.get('result')
                if not result:
                    print('No "result" key found in JSON response content.')
                    sys.exit(0)
                else:
                    return result

def get_organization_data(organization):
    """Return dict of organization data from a CKAN dataset.

    Parameters:
    organization (dict): CKAN organization

    """
    # Get the data.
    publisher = {}
    publisher['title'] = organization.get('title', '')
    publisher['id'] = organization.get('name', '')
    if publisher['id']:
        publisher['homepage'] = 'http://data.gov.uk/publisher/' + publisher['id']
    else:
        publisher['homepage'] = ''
    for extra in organization.get('extras', []):
        if extra.get('key') == 'category':
            publisher['type'] = extra.get('value', '')
        elif extra.get('key') == 'contact-name':
            publisher['contact'] = extra.get('value', '')
        elif extra.get('key') == 'contact-email':
            publisher['email'] = re.sub('mailto:|email ', '', extra.get('value', ''))
    organization_groups = get_organization_groups(organization)
    if len(organization_groups) == 1:
        publisher['parent_id'] = organization_groups[0]
    else:
        publisher['parent_id'] = ''

    return publisher

def get_organization_groups(organization):
    """Recursively find the most general groups the organization is part of."""
    parent_groups = []
    for group in organization.get('groups', []):
        if group.get('groups'):
            parent_group = get_organization_groups(group)
        else:
            parent_group = group['name']
        parent_groups.append(parent_group)
    return parent_groups

def relevant_publishers(filepath=os.path.join(DATA_DIR, 'publisher_lookup.csv')):
    """Define the list of publishers for which data is wanted

    Parameters:
    filepath (path): File containing normalized instition names(ex: ministry-of-defence)

    """
    with open(filepath, mode='r') as f:
        data = {}
        reader = csv.DictReader(f)
        for row in reader:
            for header, value in row.items():
                try:
                    data[header].append(value)
                except KeyError:
                    data[header] = [value]

    relevant_publishers = data['normalized_name']

    return relevant_publishers


def get_all_organizations(url_base):
    """Return list of publishers."""
    # Get organizations.
    url = url_base + '3/action/organization_list?all_fields=True&include_groups=True&include_extras=True'
    print('Scraping publishers...')
    organization_list = import_dataset(url)
    time.sleep(0.3)
    print('Scraping publishers... Done')

    # Get data for each organization.
    print('Loading publishers data...')
    publishers = []
    for organization in organization_list:
        # Scrape only the relevant publishers.
        if organization.get('name') in relevant_publishers():
            organization_data = get_organization_data(organization)
            publishers.append(organization_data)

    print('Loading publishers data... Done')
    print('Scraped: ' + str(len(publishers)) + ' publishers')

    return publishers

def get_count(url):
    """Return number of results.

    Parameters:
    url (str): url with a query

    """
    result = import_dataset(url)
    # Get the count.
    count = result.get('count', '')
    return int(count)

def get_number_pages(count):
    """Return the number of pages for 1000 results per page."""
    pages = math.ceil(float(count) / 1000)
    return int(pages)

def get_results(url_base, query):
    """Return result packages.

    Parameters:
    url_base (str): CKAN API url
    query (str): query to search for packages

    """
    # Get the number of results.
    url_count = 'http://data.gov.uk/api/action/package_search?q=' + query + '&rows=1'
    print('Scraping number of packages...')
    count = get_count(url_count)
    print('Scraping number of packages... Done')
    print('Number of packages to scrape: ' + str(count))
    time.sleep(0.3)

    # Get the number of pages.
    pages = get_number_pages(count)
    print('Maximum number of packages per page: 1000')
    print('Number of results pages to scrape: ' + str(pages))

    # Get the results.
    print('Scraping packages...')
    results = []
    for i in range(0, pages):
        url = url_base + 'action/package_search?q=' + query + '&rows=1000&start=' + str(i * 1000)
        result = import_dataset(url)
        time.sleep(0.3)
        if result.get('results'):
            results.append(result['results'])
    print('Scraping packages... Done')

    return results


def get_datafile_data(package, resource):
    """Return dict of data of a resource.

    Parameters:
    package (dict): CKAN package
    resource (dict): CKAN resource from package

    """
    # Get data of datafile.
    datafile = {}
    datafile['id'] = resource.get('id', '')
    url = resource.get('url', '').strip(' ')
    datafile['data'] =  re.sub('\/$', '', url)
    datafile['format'] = clean_format(datafile['data'])

    datafile['last_modified'] = resource.get('last_modified', '')

    title = package.get('title', '')
    description = resource.get('description', '')
    datafile['title'] = '/'.join(string for string in [title, description] if string )

    datafile['publisher_id'] = package.get('organization', {}).get('name', '')
    datafile['schema'] = SCHEMA
    for possible_name in  ['created', 'created_at', 'date_released', 'date']:
        datafile['created_at'] = resource.get(possible_name, '') or package.get(possible_name, '')
        if datafile['created_at']:
            break
    return datafile


def get_datafiles(package, publishers):
    """Return list of datafiles of a package.

    Parameters:
    package (dict): CKAN package

    """
    datafiles = []
    # Scrape only ministerial departments data
    package_publisher = package.get('organization', {}).get('name', '')
    for publisher in publishers:
        if package_publisher == publisher['id']:
            for resource in package['resources']:
                datafile = get_datafile_data(package, resource)

                if datafile['format'] in ['csv', 'excel', '']:
                    datafiles.append(datafile)
    return datafiles

def make_csv(csvfile, fieldnames, dataset):
    """Create a csv file.

    Parameters:
    csvfile (str): name of csv file to create
    fieldnames (list of str): csv header
    dataset (list of dict): each dict will be a csv row

    """
    with open(csvfile, mode='w+t', encoding='utf-8') as data:
        writer = csv.DictWriter(data, fieldnames=fieldnames, lineterminator=os.linesep)
        writer.writeheader()
        for element in dataset:
            writer.writerow(element)

def make_publishers_csv(csvfile):
    """Make publishers csv file."""
    # Get organizations data
    publishers = get_all_organizations('http://data.gov.uk/api/')

    # Make publishers csv file.
    fieldnames = ['id', 'title', 'type', 'homepage', 'contact', 'email', 'parent_id']
    print('Making ' + csvfile + '...')
    make_csv(csvfile, fieldnames, publishers)
    print('Making ' + csvfile + '... Done')
    return publishers

def make_datafiles_csv(csvfile, publishers):
    """Make datafiles csv file."""
    # Get results from http://data.gov.uk/.
    url_base = 'http://data.gov.uk/api/'
    # Apache Solr search query for spending files.
    search_query = urllib.parse.quote('title:(over AND 25) OR description:(over AND 25) OR name:(over AND 25)')
    print('Scraping sources...')
    results = get_results(url_base, search_query)
    print('Scraping sources... Done')

    # Get datafiles from results.
    resources = []
    package_count = 0
    print('Loading sources data...')
    for page in results:
        for package in page:
            datafiles = []
            if 'unpublished' in package:
                if package['unpublished'] != 'true':
                    datafiles = get_datafiles(package, publishers)
                    resources += datafiles
            else:
                datafiles = get_datafiles(package, publishers)
                resources += datafiles
        package_count += len(page)
    print('Loading sources data... Done')
    print('Scraped: ' + str(len(resources)) + ' sources.')

    # Make datafiles csv file.
    fieldnames = ['id', 'publisher_id', 'title', 'data', 'format', 'last_modified',
                  'schema', 'created_at']
    print('Making ' + csvfile + '...')
    unique_resources = {v['data']:v for v in resources}.values()
    make_csv(csvfile, fieldnames, unique_resources)
    print('Making ' + csvfile + '... Done')

def clean_format(url):
    """Return cleaned format string.

    Parameters:
    url (str): url of the resource

    """
    formats = { 'csv': '\.csv$', 'excel': '\.xls[xm]?$', 'pdf': '\.pdf$',
    'xml': '\.xml$', 'html': '\.(html|htm|php|aspx)$', 'zip': '\.zip$',
    'ods': '\.ods$', 'doc': '\.doc[x]?$', 'json': '\.json$', 'txt': '\.txt$'}
    # Get format from file extension or format value in resource

    for file_format, rule in formats.items():
        if re.search(rule, url, re.I):
            break
    else:
        file_format = ''

    try:
        resource_request = open_resource_url(url)
        if file_format == '' and not isinstance(resource_request, int) and \
            is_html(resource_request):
            file_format = 'html'
    except urllib.error.URLError as e:
        file_format = 'unknown'

    return file_format


def is_html(content):
    """Return true if is an html file.

    Parameters:
    content (str): content of the resource

    """

    html = BeautifulSoup(content, 'html.parser').find()
    if html:
        return True
    else:
        return False

def open_resource_url(data_url):
    """Return resource content or http error status.

    Parameters:
    data_url (str): url of the resource

    """
    data_surce = urllib.request.Request(data_url)
    try:
        content = urllib.request.urlopen(data_surce)
        return content
    except urllib.error.HTTPError as e:
        return e.getcode()
    except urllib.error.URLError as e:
        raise e

# Scrape all ministerial departments data.
publishers = make_publishers_csv(PUBLISHER_FILEPATH)
make_datafiles_csv(SOURCE_FILEPATH, publishers)
