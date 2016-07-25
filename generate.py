#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cubing

import argparse
from bs4 import BeautifulSoup
import ConfigParser
import csv
import datetime
import glob
from jinja2 import Environment, FileSystemLoader
import os
import re
import urllib2
import zipfile


SCRIPT_DIR            = os.path.abspath(os.path.dirname(__file__))
WCA_EXPORT_DIR        = '/WCA_export'
WCACOUNTRIES_FILENAME = 'WCA_export_Countries.tsv'
WCARESULTS_FILENAME   = 'WCA_export_Results.tsv'
PSYCH_TEMPLATE        = 'psych.tpl'

WCA_EXPORT_URL        = 'https://www.worldcubeassociation.org/results/misc'

VALUE_DNF = 9999999999


def read_compinfo(comp):
    """ Reads competition info (name and description) from .txt """
    config = ConfigParser.SafeConfigParser()
    config.read(comp + '.txt')
    return {'name': config.get('competition', 'name').decode('utf-8'),
            'description': config.get('competition', 'description').decode('utf-8')}


def read_compdata(comp):
    """ Reads competition data from .csv """
    csvdata, competitorsname, competitorscountry, entries = [], {}, {}, {}

    # Store CSV into dict
    with open(comp + '.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            csvdata.append([item.decode('utf-8').strip() for item in row])

    # Assing ID for new competitors
    n = 1
    for i, row in enumerate(csvdata):
        if row[0] == '0':
            csvdata[i][0] = 'N_%03d' % (n)
            n = n + 1

    # header -> events
    events = [item for item in csvdata[0] if item in cubing.EVENTS_ALL]
    # first column -> competitors
    competitors = [row[0] for row in csvdata[1:]]

    # generate entry info
    for row in csvdata[1:]:
        competitor_id = row[0]
        competitorsname[competitor_id] = row[-1]
        competitorscountry[competitor_id] = 'Unknown'
        entries[competitor_id] = {}
        for i, flag in enumerate(row[1:-1]):
            if flag != '':
                entries[competitor_id][events[i]] = True
            else:
                entries[competitor_id][events[i]] = False

    return {'events': events, 'competitors': competitors,
            'competitorsname': competitorsname, 'competitorscountry': competitorscountry,
            'entries': entries}


def download_export():
    """ Downloads the latest WCA export. """
    html = urllib2.urlopen(WCA_EXPORT_URL + '/export.html')
    soup = BeautifulSoup(html, 'html.parser')
    latest = soup.find('dl').find_all('a', href=re.compile('tsv'))[0].get('href')
    zippath = SCRIPT_DIR + WCA_EXPORT_DIR + '/' + latest
    if not os.path.isfile(zippath):
        with open(zippath, 'wb') as file:
            file.write(urllib2.urlopen(WCA_EXPORT_URL + '/' + latest).read())


def find_latest_export():
    """ Finds the latest WCA export in `WCA_export` directory. """
    files = glob.glob(SCRIPT_DIR + WCA_EXPORT_DIR + '/WCA_export*.tsv.zip')
    files_dict = {os.path.basename(file)[14:22]: os.path.basename(file) for file in files}
    return sorted(files_dict.items())[-1][1]


def read_wcacountries(latest_export):
    """ Reads the WCA countries. """
    countries = {'Unknown': {'name': 'Unknown', 'iso2': '_unknown'}}

    # Read countries data
    with zipfile.ZipFile(SCRIPT_DIR + WCA_EXPORT_DIR + '/' + latest_export) as zf:
        with zf.open(WCACOUNTRIES_FILENAME, 'r') as f:
            next(f)
            for line in f:
                items = line.decode('utf-8').strip().split('\t')
                countries[items[0]] = {'name': items[2], 'iso2': items[6]}

    return countries


def read_wcaresults(compdata, countries, latest_export):
    """ Reads the WCA results. Returns data for psych sheets. """
    raw = {}

    # Initialization with events
    for event in compdata['events']:
        raw[event] = {}

    # Read raw data
    with zipfile.ZipFile(SCRIPT_DIR + WCA_EXPORT_DIR + '/' + latest_export) as zf:
        with zf.open(WCARESULTS_FILENAME, 'r') as f:
            next(f)
            for line in f:
                items = line.decode('utf-8').split('\t')
                event_id, best, average = items[1], items[4], items[5]
                person_name, person_id, person_country = items[6], items[7], items[8]
                if (event_id in compdata['events']) and (person_id in compdata['competitors']):
                    compdata['competitorsname'][person_id] = person_name
                    compdata['competitorscountry'][person_id] = person_country
                    if compdata['entries'][person_id][event_id]:
                        record = -1
                        if event_id in cubing.EVENTS_BEST:
                            record = int(best)
                        elif event_id in cubing.EVENTS_AVERAGE:
                            record = int(average)
                        if (0 < record) and \
                           ((person_id not in raw[event_id]) or (record < raw[event_id][person_id]['value'])):
                            raw[event_id][person_id] = {'id': person_id, 'name': person_name,
                                                        'country': person_country,
                                                        'countryiso2': countries[person_country]['iso2'],
                                                        'value': record,
                                                        'formatted': cubing.format_record(record, event_id),
                                                        'haswcaid': True}

    # Update new competitors
    for event in compdata['events']:
        for competitor_id, entries in compdata['entries'].items():
            if compdata['entries'][competitor_id][event] and competitor_id not in raw[event]:
                competitor_country = compdata['competitorscountry'][competitor_id]
                raw[event][competitor_id] = {'id': competitor_id,
                                             'name': compdata['competitorsname'][competitor_id],
                                             'country': competitor_country,
                                             'countryiso2': countries[competitor_country]['iso2'],
                                             'value': VALUE_DNF, 'formatted': '&ndash;',
                                             'haswcaid': competitor_id[0] != 'N'}

    return raw


def generate_psych(wcaresults):
    """ Generates psych data by sorting. """
    psych = {}
    for event_id, event_result in wcaresults.items():
        noobs = {}
        psych[event_id] = []
        print 'In the event of %s......' % (event_id)
        n = 1
        for competitor_id, record in sorted(event_result.items(), key=lambda x:x[1]['value']):
            record['rank'] = n
            if record['value'] < VALUE_DNF:
                psych[event_id].append(record)
                print '  #%d %s achieves %s' % (n, competitor_id, record['formatted'])
                n = n + 1
            else:
                noobs[competitor_id] = record

        for competitor_id, record in sorted(noobs.items(), key=lambda x:x[1]['id']):
            psych[event_id].append(record)
            print '  #%d %s is noob' % (n, competitor_id)

    return psych


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Psych sheets generator')
    parser.add_argument('competition', nargs=None, default=None, type=str,
                        help='Input competition name')
    parser.add_argument('--output', '-o', default='psych.html', type=str,
                        help='Path to output html')
    parser.add_argument('--list', '-l', default=False, action='store_true',
                        help='Print list of competitors')
    parser.add_argument('--count', '-c', default=None, type=str,
                        help='Count competitors in the specified event (e.g. --count=333,444,555 means it counts ones who participate in 333, 444, or 555)')
    args = parser.parse_args()

    # Read competition
    compinfo = read_compinfo(args.competition)
    compdata = read_compdata(args.competition)

    # Read WCA results and generate psych
    download_export()
    latest_export = find_latest_export()
    wcacountries = read_wcacountries(latest_export)
    wcaresults = read_wcaresults(compdata, wcacountries, latest_export)

    if args.list_competitors:
        for competitor in compdata['competitors']:
            print competitor, compdata['competitorsname'][competitor]

    elif args.count:
        n = 0
        for wcaid, events in compdata['entries'].items():
            for e in args.count.split(','):
                if events[e]:
                    print wcaid
                    n = n + 1
                    break
        print n

    else:
        # Generate psych
        psych = generate_psych(wcaresults)

        # Generate html
        dt = datetime.datetime.fromtimestamp(os.stat(SCRIPT_DIR + WCA_EXPORT_DIR + '/' + latest_export).st_mtime)
        attrs = {'events_name': cubing.EVENTS_NAME, 'database_version': latest_export.split('.')[0],
                 'date_fetched': dt.strftime('%Y-%m-%d')}
        env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
        tpl = env.get_template(PSYCH_TEMPLATE)
        html = tpl.render({'attrs': attrs, 'compinfo': compinfo, 'compdata': compdata, 'psych': psych})
        with open(args.output, 'w') as f:
            f.write(html.encode('utf-8'))
        print 'Complete writing to %s' % (args.output)
