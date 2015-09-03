#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cubing

import argparse
import ConfigParser
import csv
import glob
from jinja2 import Environment, FileSystemLoader
import os
import zipfile


#COMPETITORS_FILENAME = 'competitors.txt'
#EVENTS_FILENAME      = 'events.txt'
WCARESULTS_FILENAME  = 'WCA_export_Results.tsv'
PSYCH_TEMPLATE       = 'psych.tpl'
PSYCH_HTML           = 'psych.html'

SCRIPT_DIR     = os.path.abspath(os.path.dirname(__file__))
WCA_EXPORT_DIR = '/WCA_export'


def read_compinfo(comp):
    """ Reads competition info (name and description) from .txt """
    config = ConfigParser.SafeConfigParser()
    config.read(comp + '.txt')
    return {'name': config.get('competition', 'name'),
            'description': config.get('competition', 'description')}


def read_compdata(comp):
    """ Reads competition data from .csv """
    csvdata, events, competitors, entries = [], [], [], {}

    # Store CSV into dict
    with open(comp + '.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            csvdata.append([item.replace(' ', '') for item in row])

    # header -> events
    events = csvdata[0][1:]

    # first item -> competitors
    competitors = [row[0] for row in csvdata[1:]]

    # generate entry info
    for row in csvdata[1:]:
        competitor_id = row[0]
        entries[competitor_id] = {}
        for i, flag in enumerate(row[1:]):
            if flag != '':
                entries[competitor_id][events[i]] = True
            else:
                entries[competitor_id][events[i]] = False

    return {'events': events, 'competitors': competitors, 'entries': entries}


def find_latest_export():
    """ Finds the latest WCA export in `WCA_export` directory. """
    files = glob.glob(SCRIPT_DIR + WCA_EXPORT_DIR + '/WCA_export*.tsv.zip')
    filesd = {os.path.basename(file)[14:22]: os.path.basename(file) for file in files}
    return filesd.items()[-1][1]


def read_wcaresults(compdata, latest_export):
    """ Reads the WCA results. Returns data for psych sheets. """
    raw, psych = {}, {}

    # Initialization with events
    for e in compdata['events']:
        raw[e] = {}

    # Read raw data
    with zipfile.ZipFile(SCRIPT_DIR + WCA_EXPORT_DIR + '/' + latest_export) as zf:
        with zf.open(WCARESULTS_FILENAME, 'r') as f:
            next(f)
            for line in f:
                items = line.split('\t')
                event_id, best, average = items[1], items[4], items[5]
                person_name, person_id = items[6], items[7]
                if (event_id in compdata['events']) and (person_id in compdata['competitors']) and \
                   compdata['entries'][person_id][event_id]:
                    record = -1
                    if event_id in cubing.EVENTS_BEST:
                        record = int(best)
                    elif event_id in cubing.EVENTS_AVERAGE:
                        record = int(average)
                    if 0 < record:
                        # Store the record
                        if (person_id not in raw[event_id]) or (record < raw[event_id][person_id]['value']):
                            raw[event_id][person_id] = {'value': record,
                                                        'formatted': cubing.format_record(record, event_id),
                                                        'id': person_id, 'name': person_name.decode('utf-8')}

    # Sort by record
    for ek, ev in raw.items():
        psych[ek] = []
        print 'In the event of %s......' % (ek)
        for k, v in sorted(ev.items(), key=lambda x:x[1]['value']):
            psych[ek].append(v)
            print '  %s achieves %s' % (k, v['formatted'])

    return psych


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Psych sheets generator')
    parser.add_argument('competition', nargs=None, default=None, type=str,
                        help='Input competition name')
    parser.add_argument('--output', '-o', default='psych.html', type=str,
                        help='Path to output html')
    args = parser.parse_args()

    # Read competition
    compinfo = read_compinfo(args.competition)
    compdata = read_compdata(args.competition)
    print 'compinfo:', compinfo
    print 'compdata:', compdata

    # Read WCA results and store them
    latest_export = find_latest_export()
    print 'latest_export:', latest_export
    psych = read_wcaresults(compdata, latest_export)
    print 'psych: ', psych

    # Generate html
    env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
    tpl = env.get_template(PSYCH_TEMPLATE)
    attrs = {'events_name': cubing.EVENTS_NAME, 'database_version': latest_export.split('.')[0]}
    html = tpl.render({'attrs': attrs, 'compinfo': compinfo, 'compdata': compdata, 'psych': psych})
    with open(args.output, 'w') as f:
        f.write(html.encode('utf-8'))
    print 'Complete writing to %s' % (args.output)
