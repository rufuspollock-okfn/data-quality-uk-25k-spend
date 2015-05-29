# -*- coding: utf-8 -*-
"""This script makes a CSV performance file for publishers.

"""

import os
import csv
import datetime
import time
import math

# Files path.
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data'))
PUBLISHERS_FILEPATH = os.path.join(DATA_DIR, 'publishers.csv')
SOURCES_FILEPATH = os.path.join(DATA_DIR, 'sources.csv')
RESULTS_FILEPATH = os.path.join(DATA_DIR, 'results.csv')
PERFORMANCE_FILEPATH = os.path.join(DATA_DIR, 'performance.csv')

def get_publishers(publishers_file):
    """Return list of publishers id. """

    print('Getting publishers...')
    publishers = []
    with open(publishers_file, mode='r') as publishers_data:
        reader = csv.DictReader(publishers_data)
        for row in reader:
            publishers.append(row['id'])
    print('Getting publishers... Done')
    print(str(len(publishers)) + ' publishers.')
    return publishers

def get_source_score(source_id, results_file):
    """Return latest score of a source from results. """

    score = 0
    latest_timestamp = 0
    with open(results_file, mode='r') as results_data:
        reader = csv.DictReader(results_data)
        for row in reader:
            if row['source_id'] == source_id:
                timestamp = time.mktime(datetime.datetime.strptime(row['timestamp'], '%Y-%m-%dT%H:%M:%S.%f+00:00').timetuple())
                if timestamp > latest_timestamp:
                    latest_timestamp = timestamp
                    score = int(row['score']) * 10
    return score

def get_sources(publisher_id, sources_file, results_file):
    """Return list of sources of a publisher with id, period and score. """

    sources = []
    with open(sources_file, mode='r') as sources_data:
        reader = csv.DictReader(sources_data)
        for row in reader:
            source = {}
            if row['publisher_id'] == publisher_id:
                source['id'] = row['id']
                if row['period_id']:
                    period = row['period_id'].split('/')
                    if len(period) == 1:
                        source['period_id'] = period[0]
                    elif len(period) == 2:
                        source['period_id'] = period[1]
                else:
                    source['period_id'] = ''
                source['score'] = get_source_score(source['id'], results_file)
                sources.append(source)
    return sources

def get_periods(sources):
    """Return list of unique periods from sources. """

    periods = []
    for source in sources:
        if source['period_id']:
            periods.append(source['period_id'])
    periods = list(set(periods))
    return periods

def get_period_sources(period, sources):
    """Return list of sources for a period. """

    period_sources = []
    for source in sources:
        if period == source['period_id']:
            period_sources.append(source)
    return period_sources

def get_period_score(period_sources):
    """Return average score from list of sources. """

    score = 0
    if len(period_sources) > 0:
        total = 0
        for source in period_sources:
            total += int(source['score'])
        score = round(total / len(period_sources))
    return score

def get_period_valid(period_sources):
    """Return valid percentage from list of sources. """

    valid = 0
    if len(period_sources) > 0:
        valids = []
        for source in period_sources:
            if int(source['score']) == 100:
                valids.append(source)
        if valids:
            valid = round(len(valids) / len(period_sources) * 100)
    return valid

def get_periods_data(publihser_id, periods, sources):
    """Return list of performances for a publisher, by period. """

    performances = []
    period_sources_to_date = []
    for period in periods:
        period_sources = get_period_sources(period, sources)
        period_sources_to_date += period_sources
        performance = {}
        performance['publisher_id'] = publihser_id
        performance['period_id'] = period
        performance['files_count'] = len(period_sources)
        performance['score'] = get_period_score(period_sources)
        performance['valid'] = get_period_valid(period_sources)
        performance['score_to_date'] = get_period_score(period_sources_to_date)
        performance['valid_to_date'] = get_period_valid(period_sources_to_date)
        performance['files_count_to_date'] = len(period_sources_to_date)
        performances.append(performance)
    return performances

def get_all_periods(periods):
    """Return all periods from oldest in periods to now. """

    # Get oldest period.
    current_date = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    oldest_date = current_date
    oldest_timestamp = time.mktime(datetime.datetime.strptime(oldest_date, '%Y-%m-%d').timetuple())
    for period in periods:
        timestamp = time.mktime(datetime.datetime.strptime(period, '%Y-%m-%d').timetuple())
        if timestamp < oldest_timestamp:
            oldest_timestamp = timestamp
            oldest_date = period

    # Get all periods.
    all_periods = []
    oldest_date_data = oldest_date.split('-')
    oldest_year = int(oldest_date_data[0])
    oldest_month = int(oldest_date_data[1])
    current_date_data = current_date.split('-')
    current_year = int(current_date_data[0])
    current_month = int(current_date_data[1])

    for i in range(oldest_month, 13):
        period = str(oldest_year) + '-' + str(i).zfill(2) + '-01'
        all_periods.append(period)

    for i in range(oldest_year + 1, current_year):
        for j in range(1, 13):
            period = str(i) + '-' + str(j).zfill(2) + '-01'
            all_periods.append(period)

    for i in range(1, current_month + 1):
        period = str(current_year) + '-' + str(i).zfill(2) + '-01'
        all_periods.append(period)

    return all_periods

def make_performance(performance_file, publishers):
    """Make a performance CSV file for all publishers. """

    with open(performance_file, mode='w') as performance_data:
        fieldnames = ['publisher_id', 'period_id', 'files_count', 'score', 'valid', 'files_count_to_date', 'score_to_date', 'valid_to_date']
        writer = csv.DictWriter(performance_data, fieldnames=fieldnames)
        writer.writeheader()

        # Get all periods.
        print('Getting periods...')
        available_periods = []
        for publisher in publishers:
            sources = get_sources(publisher, SOURCES_FILEPATH, RESULTS_FILEPATH)
            periods = get_periods(sources)
            available_periods += periods
        all_periods = get_all_periods(available_periods)
        print('Getting periods... Done')
        periods_length = len(all_periods)
        print(str(periods_length) + ' periods from ' + all_periods[0] + ' to ' + all_periods[periods_length - 1] + '.')

        # Get performances for each publisher.
        print('Getting publishers performances...')
        publishers_performances = []
        all_sources = []
        for publisher in publishers:
            sources = get_sources(publisher, SOURCES_FILEPATH, RESULTS_FILEPATH)
            performances = get_periods_data(publisher, all_periods, sources)
            publishers_performances += performances
            all_sources += sources
            for performance in performances:
                writer.writerow(performance)
        print('Getting publishers performances... Done')

        # Get performances for all publishers.
        print('Getting all publishers performances...')
        all_performances = get_periods_data('all', all_periods, all_sources)
        for performance in all_performances:
            writer.writerow(performance)
        print('Getting all publishers performances... Done')
        print(str(len(publishers_performances) + len(all_performances)) + ' rows in ' + performance_file + '.')

# Get publishers.
publishers = get_publishers(PUBLISHERS_FILEPATH)
# Make performance file.
make_performance(PERFORMANCE_FILEPATH, publishers)
