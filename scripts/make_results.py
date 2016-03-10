# -*- coding: utf-8 -*-
"""This script makes the final results and runs CSV files.

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import os
import csv
import uuid

# Files path.
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data'))
SOURCE_FILEPATH = os.path.join(DATA_DIR, 'sources.csv')
INVALID_SOURCE_FILEPATH = os.path.join(DATA_DIR, 'invalid_sources.csv')
RESULTS_FILEPATH = os.path.join(DATA_DIR, 'results.csv')
FINAL_RESULTS_FILEPATH = os.path.join(DATA_DIR, 'final_results.csv')
RUNS_FILEPATH = os.path.join(DATA_DIR, 'runs.csv')
FINAL_RUNS_FILEPATH = os.path.join(DATA_DIR, 'final_runs.csv')

def make_results(results, sources, invalid_sources, final_results):
    """Make the final results CSV file. """

    scores = []
    with open(final_results, mode='w') as final:
        fieldnames = ['id', 'source_id', 'publisher_id', 'period_id', 'score', 'data', 'schema', 'summary', 'run_id', 'timestamp', 'report']
        writer = csv.DictWriter(final, fieldnames=fieldnames)
        writer.writeheader()

        with open(results, mode='r') as tmp:
            results_reader = csv.reader(tmp)
            results_data = {}

            with open(sources, mode='r') as data:
                sources_reader = csv.DictReader(data)

                for row in results_reader:
                    final_row = {}
                    if not results_data:
                        results_data['run_id'] = row[8]
                        results_data['timestamp'] = row[9]
                        results_data['report'] = row[10]
                    source_id = row[1]
                    url = ''
                    for source_row in sources_reader:
                        if source_row['id'] == source_id:
                            url = source_row['data']
                    data.seek(0)
                    final_row['data'] = url
                    final_row['id'] = row[0]
                    final_row['source_id'] = row[1]
                    final_row['publisher_id'] = row[2]
                    final_row['period_id'] = row[3]
                    final_row['score'] = row[4]
                    final_row['schema'] = row[6]
                    final_row['summary'] = row[7]
                    final_row['run_id'] = row[8]
                    final_row['timestamp'] = row[9]
                    final_row['report'] = row[10]
                    writer.writerow(final_row)
                    scores.append(int(final_row['score']))

        with open(invalid_sources, mode='r') as invalid:
            invalid_reader = csv.DictReader(invalid)

            with open(sources, mode='r') as data:
                sources_reader = csv.DictReader(data)

                for row in invalid_reader:
                    final_row = {}
                    source_id = row['id']
                    url = ''
                    for source_row in sources_reader:
                        if source_row['id'] == source_id:
                            url = source_row['data']
                    data.seek(0)
                    final_row['data'] = url
                    final_row['id'] = uuid.uuid4().hex
                    final_row['source_id'] = row['id']
                    final_row['publisher_id'] = row['publisher_id']
                    final_row['period_id'] = row['period_id']
                    final_row['score'] = 0
                    final_row['schema'] = ''
                    final_row['summary'] = ''
                    final_row['run_id'] = results_data['run_id']
                    final_row['timestamp'] = results_data['timestamp']
                    final_row['report'] = results_data['report']
                    writer.writerow(final_row)
                    scores.append(int(final_row['score']))
    return scores

def make_runs(runs, final_runs, scores):
    """Make the final runs CSV file. """

    # Get total score.
    total = 0
    for score in scores:
        total += score
    total_score = int(round(total / len(scores)))

    # Write final runs file.
    with open(final_runs, mode='w') as final:
        fieldnames = ['id', 'timestamp', 'total_score']
        writer = csv.DictWriter(final, fieldnames=fieldnames)
        writer.writeheader()

        with open(runs, mode='r') as run:
            reader = csv.reader(run)
            for row in reader:
                final_row = {}
                final_row['id'] = row[0]
                final_row['timestamp'] = row[1]
                final_row['total_score'] = total_score
                writer.writerow(final_row)

# Make the final results CSV file.
scores = make_results(RESULTS_FILEPATH, SOURCE_FILEPATH, INVALID_SOURCE_FILEPATH, FINAL_RESULTS_FILEPATH)
make_runs(RUNS_FILEPATH, FINAL_RUNS_FILEPATH, scores)
