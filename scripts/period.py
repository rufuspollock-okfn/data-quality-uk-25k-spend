# -*- coding: utf-8 -*-
"""This module provides functions to find the period id of a source.

"""

import csv
import re
import calendar

def months_year(title, months, months_number):
    """Return period id from string title with 2 months and a year. """

    period = ''
    day = '01'
    match = re.findall(months + '(?: )+to(?: )+' + months + '(?: )*(20[0-9]{2})(?:[^0-9]|$)', title, re.I)
    if len(match) == 1:
        year = match[0][2]
        month = str(months_number[match[0][0].lower()]).zfill(2)
        end_year = match[0][2]
        end_month = str(months_number[match[0][1].lower()]).zfill(2)
        period = year + '-' + month + '-' + day + '/' + end_year + '-' + end_month + '-' + day
    return period

def month_year(title, months, months_number):
    """Return period id from string title with a month and a year. """

    period = ''
    day = '01'
    match = re.findall(months + '(?: |-)*(20[0-9]{2})(?:[^0-9]|$)', title, re.I)
    if len(match) == 2:
        year = match[0][1]
        month = str(months_number[match[0][0].lower()]).zfill(2)
        end_year = match[1][1]
        end_month = str(months_number[match[1][0].lower()]).zfill(2)
        period = year + '-' + month + '-' + day + '/' + end_year + '-' + end_month + '-' + day
    elif len(match) == 1:
        year = match[0][1]
        month = str(months_number[match[0][0].lower()]).zfill(2)
        period = year + '-' + month + '-' + day
    return period

def year_month(title, months, months_number):
    """Return period id from string title with a year and a month. """

    period = ''
    day = '01'
    match = re.findall('(?:[^0-9]|^)(20[0-9]{2})(?: )*' + months, title, re.I)
    if len(match) == 2:
        year = match[0][0]
        month = str(months_number[match[0][1].lower()]).zfill(2)
        end_year = match[1][0]
        end_month = str(months_number[match[1][1].lower()]).zfill(2)
        period = year + '-' + month + '-' + day + '/' + end_year + '-' + end_month + '-' + day
    elif len(match) == 1:
        year = match[0][0]
        month = str(months_number[match[0][1].lower()]).zfill(2)
        period = year + '-' + month + '-' + day
    return period

def qtr_years(title):
    """Return period id from string title with a quarter 'qtr' and 2 years. """

    period = ''
    day = '01'
    match = re.findall('qtr(?: )*([0-9])(?: |-)+(20[0-9]{2})-([0-9]{2})(?:[^0-9]|$)', title, re.I)
    if len(match) == 1:
        if match[0][0] == '1':
            year = match[0][1]
            month = '04'
            end_year = match[0][1]
            end_month = '06'
            period = year + '-' + month + '-' + day + '/' + end_year + '-' + end_month + '-' + day
        elif match[0][0] == '2':
            year = match[0][1]
            month = '07'
            end_year = match[0][1]
            end_month = '09'
            period = year + '-' + month + '-' + day + '/' + end_year + '-' + end_month + '-' + day
        elif match[0][0] == '3':
            year = match[0][1]
            month = '10'
            end_year = match[0][1]
            end_month = '12'
            period = year + '-' + month + '-' + day + '/' + end_year + '-' + end_month + '-' + day
        elif match[0][0] == '4':
            year = '20' + match[0][2]
            month = '01'
            end_year = '20' + match[0][2]
            end_month = '03'
            period = year + '-' + month + '-' + day + '/' + end_year + '-' + end_month + '-' + day
    return period

def years_qtr(title):
    """Return period id from string title with 2 years and a quarter. """

    period = ''
    day = '01'
    match = re.findall('(20[0-9]{2})-([0-9]{2})(?: )+qtr(?: )*([0-9])(?:[^0-9]|$)', title, re.I)
    if len(match) == 1:
        if match[0][2] == '1':
            year = match[0][0]
            month = '04'
            end_year = match[0][0]
            end_month = '06'
            period = year + '-' + month + '-' + day + '/' + end_year + '-' + end_month + '-' + day
        elif match[0][2] == '2':
            year = match[0][0]
            month = '07'
            end_year = match[0][0]
            end_month = '09'
            period = year + '-' + month + '-' + day + '/' + end_year + '-' + end_month + '-' + day
        elif match[0][2] == '3':
            year = match[0][0]
            month = '10'
            end_year = match[0][0]
            end_month = '12'
            period = year + '-' + month + '-' + day + '/' + end_year + '-' + end_month + '-' + day
        elif match[0][2] == '4':
            year = '20' + match[0][1]
            month = '01'
            end_year = '20' + match[0][1]
            end_month = '03'
            period = year + '-' + month + '-' + day + '/' + end_year + '-' + end_month + '-' + day
    return period

def quarter_years(title):
    """Return period id from string title with a quarter and 2 years. """

    period = ''
    day = '01'
    match = re.findall('quarter(?: |-)([0-9]).+(20[0-9]{2})(?:-([0-9]{2}))?(?:[^0-9]|$)', title, re.I)
    if len(match) == 1:
        if match[0][0] == '1':
            year = match[0][1]
            month = '04'
            end_year = match[0][1]
            end_month = '06'
            period = year + '-' + month + '-' + day + '/' + end_year + '-' + end_month + '-' + day
        elif match[0][0] == '2':
            year = match[0][1]
            month = '07'
            end_year = match[0][1]
            end_month = '09'
            period = year + '-' + month + '-' + day + '/' + end_year + '-' + end_month + '-' + day
        elif match[0][0] == '3':
            year = match[0][1]
            month = '10'
            end_year = match[0][1]
            end_month = '12'
            period = year + '-' + month + '-' + day + '/' + end_year + '-' + end_month + '-' + day
        elif match[0][0] == '4':
            year = '20' + match[0][2]
            month = '01'
            end_year = '20' + match[0][2]
            end_month = '03'
            period = year + '-' + month + '-' + day + '/' + end_year + '-' + end_month + '-' + day
    return period

def years(title):
    """Return period id from string title with 2 years. """

    period = ''
    day = '01'
    match = re.findall('(?:[^0-9]|^)(20[0-9]{2})(?: )*(?:-|–|/)(?: )*(?:([0-9]{2})|(20[0-9]{2}))(?:[^0-9]|$)', title, re.I)
    if len(match) == 1:
        year = match[0][0]
        month = '04'
        if match[0][2]:
            end_year = match[0][2]
        elif match[0][1]:
            end_year = '20' + match[0][1]
        end_month = '03'
        period = year + '-' + month + '-' + day + '/' + end_year + '-' + end_month + '-' + day
    return period

def month_year_abbr(title, months, months_number):
    """Return period id from string title with a month and a 2 digits year. """

    period = ''
    day = '01'
    match = re.findall(months + '(?: )*(1[0-9])(?:[^0-9]|$)', title, re.I)
    if len(match) == 1:
        year = '20' + match[0][1]
        month = str(months_number[match[0][0].lower()]).zfill(2)
        period = year + '-' + month + '-' + day
    return period

def file_typo(title):
    """Return period id from string title considering typos. """

    period = ''
    day = '01'
    match = re.findall('(Februrary|Febraury)(?: )*(20[0-9]{2})(?:[^0-9]|$)', title, re.I)
    if len(match) == 1:
        year = match[0][1]
        month = '02'
        period = year + '-' + month + '-' + day
    else:
        match = re.findall('(Mary)(?: )*(20[0-9]{2})(?:[^0-9]|$)', title, re.I)
        if len(match) == 1:
            year = match[0][1]
            month = '05'
            period = year + '-' + month + '-' + day
        else:
            match = re.findall('(Novemberber)(?: )*(20[0-9]{2})(?:[^0-9]|$)', title, re.I)
            if len(match) == 1:
                year = match[0][1]
                month = '11'
                period = year + '-' + month + '-' + day
            else:
                match = re.findall('(Septemebr)(?: )*(20[0-9]{2})(?:[^0-9]|$)', title, re.I)
                if len(match) == 1:
                    year = match[0][1]
                    month = '09'
                    period = year + '-' + month + '-' + day
    return period

def search_period(string):
    """Return period id from a string. """

    # Initialize months.
    months = '('
    month_list = [v.lower() for k,v in enumerate(calendar.month_name)]
    month_list += [v.lower() for k,v in enumerate(calendar.month_abbr)]
    for month in month_list:
        if month and months == '(':
            months += month
        elif month and months != '(':
            months += '|' + month
    months += ')'
    months_number = {v.lower(): k for k,v in enumerate(calendar.month_name)}
    months_number.update({v.lower(): k for k,v in enumerate(calendar.month_abbr)})

    # Search period id.
    period = ''
    searches = []
    searches.append(months_year(string, months, months_number))
    searches.append(month_year(string, months, months_number))
    searches.append(year_month(string, months, months_number))
    searches.append(qtr_years(string))
    searches.append(years_qtr(string))
    searches.append(quarter_years(string))
    searches.append(years(string))
    searches.append(month_year_abbr(string, months, months_number))
    searches.append(file_typo(string))

    for search in searches:
        period = search
        if period:
            break

    return period

def name_error(title, url):
    """Return period id considering errors in title. """

    period = ''
    if url == 'https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/51037/Spend_20over_2025k_20Apr-May_202010-11.csv':
        period = '2010-04-01/2010-05-01'
    elif title == 'MOD: spending over £500 on a GPC for January to December 2014 / MOD\'s government procurement card spending over £500 for April 201' and url == 'https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/380663/GPC_Transparency_Data_1_to_30_April_2014.csv':
        period = '2014-04-01'
    return period

def get_period(title, url):
    """Return period id from title and url. """

    period = ''
    name = title.split(' / ')
    
    period = name_error(title, url)
    if not period and title:
        if len(name) == 2 and name[1]:
            period = search_period(name[1])
        if not period and name[0]:
            period = search_period(name[0])
        if not period and url:
            period = search_period(url)
    return period
